import RPi.GPIO as GPIO
import time
import mysql.connector
import pyautogui

# # Establish connection to the database
# db_connection = mysql.connector.connect(
#     host="your_host",
#     user="your_username",
#     password="your_password",
#     database="your_database"
# )

# username = get from website

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
timestamp = 0
bp_status = 0

def camera_on():
    return True


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
    

    try:
        while True:
            distance = calculate_distance()
            print("Distance:", distance, "cm")
            time.sleep(1)
            if distance < 100:
                person_detected = True
                print("DISTANCE <100")
                #camera_on()
            
                if (distance < min_eye_distance or distance > max_eye_distance) and body_posture == True:
                    continue
                else:
                    print("ELSE")
                    # time = 0
                    # timestamp = time.time()
                    # while body_posture == False:
                    #     time += 1
                    #     if time == 10:
                    #         screenshot = pyautogui.screenshot()
                    #         screenshot.save('screenshot.png')
                    #         timeStart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                    #         bp_status = 1
                            
                    
                    # if bp_status == 1:
                        # duration = time # or should we just use another timestamp and retrieve the minutes
                        # eyeDist = distance 
                        # insert_query = "INSERT INTO your_table_name (username, timeStart, image, duration, eyeDist) VALUES (%s, %s, %s, %s, %s)"
                        # cursor.execute(insert_query, (username, timeStart, image, duration, eyeDist))
                
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
