import RPi.GPIO as GPIO
import time
import mysql.connector
import cv2
import mediapipe as mp
import math
import time
from plyer import notification


# Establish connection to the database
db_connection = mysql.connector.connect(
    host="localhost",
    user="lucas",
    password="password",
    database="edge",
    port=3306
)

# username = get from website
username= "test1"

# Define GPIO pins (modify if you used different pins)
TRIG_PIN = 23
ECHO_PIN = 24

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

start_time = 0
end_time = 0
echo_started = False
person_detected = False
bp_status = 0

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Streamlit App",
        timeout=10  # Notification timeout in seconds
    )

def switch_on_camera(max_retries=3, retry_interval=1):
    retries = 0
    cap = None

    while retries < max_retries:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("Camera opened successfully.")
            return cap
        
        print(f"Error: Unable to open camera. Retrying in {retry_interval} seconds...")
        retries += 1
        time.sleep(retry_interval)

    print("Failed to open camera after multiple retries.")
    return None


# Function to calculate angle between two vectors
def calculate_angle(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    cosine_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle = math.degrees(math.acos(cosine_angle)) 
    
    return angle
        
def analyze_posture(cap):
    overall_feedback = "No Pose Detected"

    # Initialize the pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2)

    # Capture a photo
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with the pose model
    results = pose.process(frame_rgb)

    # Initialize drawing utils
    mp_drawing = mp.solutions.drawing_utils

    # Draw the pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Check if all required landmarks are detected
        if all(landmark in results.pose_landmarks.landmark for landmark in []):
            # Get necessary landmarks
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            # right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            # right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            # right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            # right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            # right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

            # Calculate vectors
            vector1 = (left_hip.x - left_shoulder.x, left_hip.y - left_shoulder.y)
            vector2 = (left_knee.x - left_hip.x, left_knee.y - left_hip.y)
            vector3 = (left_elbow.x - left_wrist.x, left_elbow.y - left_wrist.y)
            vector4 = (left_elbow.x - left_shoulder.x, left_elbow.y - left_shoulder.y)
            vector5 = (left_knee.x - left_ankle.x, left_knee.y - left_ankle.y)
            
            # Calculate the angles
            back_angle = 180 - calculate_angle(vector1, vector2)
            elbow_angle = calculate_angle(vector3, vector4)
            knee_angle = calculate_angle(vector2, vector5)

            # Check if angles are within specified ranges
            back_angle_feedback = "correct angle" if 90 <= back_angle <= 120 else f"wrong angle ({back_angle:.2f})"
            elbow_angle_feedback = "correct angle" if 90 <= elbow_angle <= 120 else f"wrong angle ({elbow_angle:.2f})"
            knee_angle_feedback = "correct angle" if 90 <= knee_angle <= 130 else f"wrong angle ({knee_angle:.2f})"
            overall_feedback = "Correct Posture" if all(angle_feedback.startswith("correct") for angle_feedback in [back_angle_feedback, elbow_angle_feedback, knee_angle_feedback]) else "Incorrect Posture"

            # Display the angles on the frame
            cv2.putText(frame, f"Back Angle: {back_angle_feedback}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame, f"Elbow Angle: {elbow_angle_feedback}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame, f"Knee Angle: {knee_angle_feedback}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        

    return overall_feedback, frame




# Calculate distance based on measured pulses
def calculate_distance():
    # Send trigger pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microsecond pulse
    GPIO.output(TRIG_PIN, False)

    # Wait for echo pulse to start
    while GPIO.input(ECHO_PIN) == 0:
        pass
    pulse_start = time.time()

    # Wait for echo pulse to end
    while GPIO.input(ECHO_PIN) == 1:
        pass
    pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 34300 / 2  # Divide by 2 for round trip

    return distance

def main():
    # Create a cursor object to execute SQL queries
    max_eye_distance = 76
    min_eye_distance = 30
    global stream
    cameraison = False
    

    try:
        while True:
            if(cameraison == False):
                distance = calculate_distance()
                print("Distance:", distance, "cm")
                time.sleep(1)
                
                if distance < 100:
                    person_detected = True
                    print("MAIN CODE AFTER CAMERA ON")
                    if(cameraison == False):
                        stream = switch_on_camera()
                        cameraison = True
                        print(cameraison)
                        
                    if cameraison == True:
                        print("HELO")
                        body_posture, frame = analyze_posture(stream)
                        print(body_posture)
                        while body_posture == "No Pose Detected":
                            body_posture, frame = analyze_posture(stream)
                            print(body_posture)
                            time.sleep(1)
                        print("ANALYSISING")
                        if (distance >= min_eye_distance or distance <= max_eye_distance) and body_posture == "Correct Posture":
                            print("within eye range")
                            continue
                            
                        else:
                            print("IN ELSE")
                            timeCount = 0
                            timestamp = time.time()
                            bp_status = 0
                            while(body_posture == "Incorrect Posture"):
                                body_posture, frame = analyze_posture(stream)
                                print("IN IF")
                                print(body_posture)
                                timeCount += 1
                                time.sleep(1)
                                print(timeCount)
                                if timeCount == 10:
                                    frame_bytes = cv2.imencode('posture_frame.jpg', frame)[1].tobytes()
                                    timeStart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                                    bp_status = 1
                                    continue
                            
                            if(body_posture != "Incorrect Posture" and bp_status == 1):
                                print("ITS TIME TO APPEND TO APPEND TO DB!")
                                    
                                duration = timeCount
                                    
                                eyeDist = distance
                                    
                                #initialise db cursor
                                cursor = db_connection.cursor()
                                            
                                #craft insert query with values from variables
                                insert_query = "INSERT INTO info (username, timeStart, image, duration, eyeDist) VALUES (%s, %s, %s, %s, %s)"
                                            
                                #execute and commit query
                                cursor.execute(insert_query, (username, timeStart, frame_bytes, duration, eyeDist))
                                db_connection.commit()
                                print("SUCEESS")
                                            
                                #Close the cursor and database connection
                                cursor.close()
                                bp_status = 0
                                continue
                                        
                                    #send_notification("Poor Posture Detected", "This is a notification from the Streamlit app")
                    
                
                    
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

    

    
