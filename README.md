Virtual Mouse Using Hand Gesture Recognition
This project implements a Virtual Mouse using hand gesture recognition. It leverages a webcam and computer vision to detect hand gestures and perform mouse actions such as moving the cursor, left click, right click, double-click, and even taking screenshots. The application uses OpenCV and MediaPipe to process hand landmarks and integrates with libraries like pyautogui and pynput for controlling system-level mouse operations.

Features
Move Cursor: Move the mouse cursor based on the position of your index finger.
Left Click: Perform a left-click gesture.
Right Click: Perform a right-click gesture.
Double Click: Trigger a double-click using a specific gesture.
Take Screenshots: Capture and save a screenshot with a dedicated gesture.
Libraries Used
OpenCV: For capturing video frames and rendering visual feedback.
MediaPipe: For efficient hand detection and landmark recognition.
pyautogui: To simulate mouse actions like clicks and cursor movements.
pynput: To simulate physical mouse button actions.
NumPy: For mathematical operations, such as calculating angles and distances.
Code Structure
Capture Video: The webcam feed is captured using OpenCV (cv2.VideoCapture()).
Hand Detection: MediaPipe is used to detect hand landmarks in the video frames.
Gesture Recognition:
Angles between hand landmarks are computed using trigonometry (util.get_angle).
Distances between specific landmarks are calculated (util.get_distance).
Specific gestures are detected using predefined conditions.
Mouse Control: Detected gestures are mapped to corresponding mouse actions using pyautogui and pynput.
User Feedback: Text indicating the action (e.g., "Left Click") is displayed on the video feed for visual confirmation.
How to Write the Code
Import Libraries: Import required libraries like OpenCV, MediaPipe, pyautogui, etc.
Initialize Components:
Set up MediaPipe's hand detection (mp.solutions.hands.Hands()).
Initialize the mouse controller (pynput.mouse.Controller()).
Get screen dimensions using pyautogui.size().
Hand Gesture Logic:
Detect landmarks of the hand and extract coordinates.
Define gestures based on the angle between landmarks and the distance between the thumb and index finger.
Perform Actions:
For each detected gesture, map it to mouse actions like moving the cursor, clicking, or taking a screenshot.
Run the Application:
Continuously capture webcam frames and process them in a loop.
Use OpenCV to display the video feed with hand landmarks and gesture labels.
How to Run
Install the required libraries:

pip install opencv-python mediapipe pyautogui pynput numpy
Run the script:

python virtual_mouse.py
Perform gestures in front of the webcam to control the mouse.
Index finger movement → Move the cursor
Specific gestures → Trigger actions like clicks and screenshots
Future Enhancements
Add support for multi-hand gestures.
Improve accuracy for detecting gestures.
Include additional functionalities like scrolling or drag-and-drop.
