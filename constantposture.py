import cv2
import mediapipe as mp
import math
import time
# Function to calculate the midpoint between two landmarks
def calculate_midpoint(landmark1, landmark2):
    return ((landmark1.x + landmark2.x) / 2, (landmark1.y + landmark2.y) / 2)

# Function to calculate angle between two vectors
def calculate_angle(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    cosine_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle = 180 - math.degrees(math.acos(cosine_angle)) ## i don;t know why have to use 180 to deduct but somehow make sense
    return angle

# Initialize the pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2)

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Initialize the drawing module
mp_drawing = mp.solutions.drawing_utils
start_time = time.time()
while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with the pose model
    results = pose.process(frame_rgb)

    # Draw the pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

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
        back_angle = 180-calculate_angle(vector1, vector2)
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
        if time.time() - start_time >= 1:
            print("Overall Posture:", overall_feedback)
            start_time = time.time()  # Reset the start time
    else:
            cv2.putText(frame, "Body not captured fully", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Display the frame
    cv2.imshow('Pose Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
