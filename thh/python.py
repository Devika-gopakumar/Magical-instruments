
import cv2
import numpy as np
import mediapipe as mp
import pygame


pygame.mixer.init()
sounds = {
    "bass": pygame.mixer.Sound("bass_drum.wav"),
    "snare": pygame.mixer.Sound("snare_drum.wav"),
    "cymbal": pygame.mixer.Sound("cymbal.wav")
}
zones = {
    "bass": (50, 300, 200, 450),
    "snare": (250, 300, 400, 450),
    "cymbal": (450, 300, 600, 450)
}

zone_colors = {"bass": (0, 255, 0), "snare": (255, 0, 0), "cymbal": (0, 0, 255)}
# Webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw drum zones
    for zone, (x1, y1, x2, y2) in zones.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), zone_colors[zone], 2)
        cv2.putText(frame, zone, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, zone_colors[zone], 2)

    # Detect hands
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the tip of the index finger (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            x, y = int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0])

            # Check if index finger is in any drum zone
            for zone, (x1, y1, x2, y2) in zones.items():
                if x1 < x < x2 and y1 < y < y2:
                    sounds[zone].play()  # Play corresponding sound
                    cv2.circle(frame, (x, y), 15, (255, 255, 255), -1)  # Visual feedback

    # Display the frame
    cv2.imshow("Magical Drums", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
