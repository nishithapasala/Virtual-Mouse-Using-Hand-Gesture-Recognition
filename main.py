# Import required libraries
import cv2  # For image processing and webcam handling
import mediapipe as mp  # For hand landmark detection
import util  # Utility functions for gesture calculations (custom module)
import pyautogui  # For simulating mouse movements and clicks
import random  # For generating unique filenames for screenshots
from pynput.mouse import Button, Controller  # For precise mouse controls

# Initialize mouse control
mouse = Controller()

# Get screen dimensions for mapping gesture coordinates
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe hands solution
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,  # Enables real-time gesture tracking
    model_complexity=1,  # Complexity of the hand tracking model
    min_detection_confidence=0.7,  # Minimum confidence for hand detection
    min_tracking_confidence=0.7,  # Minimum confidence for hand tracking
    max_num_hands=1  # Limit to detecting one hand
)

# Find the tip of the index finger
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None 

# Map index finger's tip coordinates to screen coordinates for mouse movement
def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)  # Map x-coordinate
        y = int(index_finger_tip.y * screen_height)  # Map y-coordinate
        pyautogui.moveTo(x, y)  # Move mouse to the mapped position

# Detect left-click gesture based on angles between landmarks and thumb-index distance
def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and  # Bent index finger
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and  # Straight middle finger
        thumb_index_dist > 50  # Distance between thumb and index is significant
    )

# Detect right-click gesture based on landmark angles
def is_right_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and  # Straight index finger
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and  # Bent middle finger
        thumb_index_dist > 50  # Thumb-index distance is significant
    )

# Detect double-click gesture based on specific hand position
def is_double_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and  # Bent index finger
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and  # Bent middle finger
        thumb_index_dist > 50  # Thumb-index distance is significant
    )

# Detect screenshot gesture based on close thumb-index distance
def is_screenshot(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and  # Bent index finger
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and  # Bent middle finger
        thumb_index_dist < 50  # Thumb-index distance is minimal
    )

# Detect gestures and perform the corresponding mouse action
def detect_gestures(frame, landmark_list, processed):
    if len(landmark_list) >= 21:  # Ensure sufficient landmarks are detected
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)  # Move the mouse pointer
        
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)  # Simulate left mouse click
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)  # Simulate right mouse click
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()  # Simulate double-click
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()  # Capture screenshot
            label = random.randint(1, 1000)  # Generate a random filename
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

# Main function to run the application
def main():
    cap = cv2.VideoCapture(0)  # Initialize webcam
    draw = mp.solutions.drawing_utils  # Helper to draw hand landmarks
    try:
        while cap.isOpened():  # Loop until the webcam is open
            ret, frame = cap.read()  # Capture frame from webcam
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

            processed = hands.process(frameRGB)  # Process the frame for hand detection
            landmark_list = []

            if processed.multi_hand_landmarks:
                hand_landmark = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmark, mpHands.HAND_CONNECTIONS)  # Draw detected hand landmarks
                for lm in hand_landmark.landmark:
                    landmark_list.append((lm.x, lm.y))
            detect_gestures(frame, landmark_list, processed)  # Detect gestures and perform actions
            cv2.imshow('Frame', frame)  # Display the video feed

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
    finally:
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == '__main__':
    main()
