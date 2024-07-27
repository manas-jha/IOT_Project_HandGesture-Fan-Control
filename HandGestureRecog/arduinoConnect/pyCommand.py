# Python script to send serial commands to the Arduino based on detected gestures
import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's serial port
time.sleep(2)  #

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def detect_gesture(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP].y
    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y

    thumb_is_up = thumb_tip < thumb_ip
    thumb_is_down = thumb_tip > thumb_ip

    fingers_are_up = (
        index_finger_tip < thumb_tip and
        middle_finger_tip < thumb_tip and
        ring_finger_tip < thumb_tip and
        pinky_tip < thumb_tip
    )
    
    fingers_are_down = (
        index_finger_tip > thumb_tip and
        middle_finger_tip > thumb_tip and
        ring_finger_tip > thumb_tip and
        pinky_tip > thumb_tip
    )

    if thumb_is_up and fingers_are_down:
        return "Thumbs Up"
    elif thumb_is_down and fingers_are_up:
        return "Thumbs Down"
    elif thumb_is_up and fingers_are_up:
        return "Open Hand"
    else:
        return "Closed Fist"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks.landmark)
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            if gesture == "Open Hand":
                arduino.write(b'O')  
            elif gesture == "Closed Fist":
                arduino.write(b'F')  
            elif gesture == "Thumbs Up":
                arduino.write(b'U') 
            elif gesture == "Thumbs Down":
                arduino.write(b'D')  

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()  # Close the serial connection
