import cv2
import mediapipe as mp
import time

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
last_print_time = time.time()
print_interval = 3 # Time interval in seconds

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    current_time = time.time()
    if current_time - last_print_time >= print_interval:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks.landmark)
                print(f"Gesture: {gesture}")
                last_print_time = current_time

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
