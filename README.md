# INF2009_T01
![image](https://github.com/bumblyowl/INF2009_T01/assets/86668765/83d3b875-b7ba-415d-83f0-89e4ef36fd67)
**Set Up**

Hardware Components:
- Raspberry Pico 400 Microcontroller
    The central processing unit is responsible for executing posture detection algorithms and managing communication with peripheral devices.
- USB Webcam
    Captures images of the user's sitting posture for analysis.
- Ultrasonic Sensors
    Detects the presence of users to activate the webcam and initiate posture monitoring. Connect to GPIO23 for TRIG and GPIO24 for ECHO


Software Components:
- Mediapipe
    Utilized for posture detection, providing real-time analysis of images captured by the webcam.
- Custom Posture Detection Algorithms
    Developed and optimized for efficient execution on the Raspberry Pico, ensuring accurate posture analysis within the device's computational capabilities.
- MariaDB
    Storing of data including images and statistics
- StreamLit
    Visualisation of data stored from a single session

  
![image](https://github.com/bumblyowl/INF2009_T01/assets/86668765/4274b6f7-f883-4652-a631-3b6fc5a43265)
**Methodology**

User Setup and Application Start:
The user sets up the hardware components, including the Raspberry Pi with ultrasonic sensor and webcam.

To wire up ultrasonic sensor, use jumper wires to connect the following:

Pi - Ultrasonic Sensor

5V - VCC
GRND - GRND
GPIO23 - TRIGGER
GPIO24 - ECHO


Connect USB webcam to Pi via USB PORT





Once powered on, the Raspberry Pi will auto-login.
User opens terminal and types the following command:

1) source myenv/bin/activate  (This activates the virtual environment)
2) cd Desktop (This changes the directory to desktop, which contains the python file to run)

For GUI to start Monitoring: 
1) python run main.py

For viewing of Dashboard:
1) streamlit run dashboard.py

After login, the user starts the application on the Raspberry Pi.

Presence Detection and Webcam Activation:
The ultrasonic sensor detects the user's presence (if the individual is within 100cm from the ultrasonic), activating the webcam.

Posture Analysis with MediaPipe Algorithm:
Video data captured by the webcam is processed through the MediaPipe algorithm on the Raspberry Pi.
MediaPipe analyzes the user's posture based on the captured video data and distance from the ultrasonic sensor.
Through research, the group decided on the justification of correct posture which is:
- an eye distance between 30 - 76cm
- an elbow angle between 90 - 120°
- a back angle (spine and leg) between 90 - 120°
- a leg angle (spine and leg) between 90 - 130°


Snapshot and Database Storage:
When an incorrect posture is detected, the system triggers a 10-second pause, allowing users to readjust their posture and enabling the system to assess if the posture adopted is not of a whim but intended by the user.
If the incorrect posture remains after a 10-second wait, the application takes a snapshot of the user's incorrect posture.
The snapshot is stored in a database for future reference and analysis.


Session End and Dashboard Access:
The user can end the session and access the dashboard through the user interface.
The dashboard displays the day's posture analysis, including posture data, notifications, and stored snapshots.

* Please refer to the main_final.py and final_final_final_dashboard.py for the most recent code for this project. The other.py files in the folder "archive" are previous drafts. 
