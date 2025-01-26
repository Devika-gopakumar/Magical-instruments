import streamlit as st
import os

# Write the Magical Drums code into a separate Python file
MAGICAL_DRUMS_FILE = "magical_drums.py"

magical_drums_code = """
import cv2
import numpy as np
import mediapipe as mp
import pygame

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame for sound
pygame.mixer.init()
sounds = {
    "bass": pygame.mixer.Sound("bass_drum.wav"),
    "snare": pygame.mixer.Sound("snare_drum.wav"),
    "cymbal": pygame.mixer.Sound("cymbal.wav")
}

# Define drum zones (x1, y1, x2, y2)
zones = {
    "bass": (50, 300, 200, 450),
    "snare": (250, 300, 400, 450),
    "cymbal": (450, 300, 600, 450)
}

# Colors for visual zones
zone_colors = {"bass": (0, 255, 0), "snare": (255, 0, 0), "cymbal": (0, 0, 255)}

# Webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally
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
"""

with open(MAGICAL_DRUMS_FILE, "w") as f:
    f.write(magical_drums_code)

# Write the Magical Guitar code into a separate Python file
MAGICAL_GUITAR_FILE = "magical_guitar.py"

magical_guitar_code = """
import cv2
import numpy as np
import mediapipe as mp
import pygame

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame for sound
pygame.mixer.init()

# Define chord sounds
chords = {
    "C": pygame.mixer.Sound("chord_c.wav"),
    "G": pygame.mixer.Sound("chord_g.wav"),
    "D": pygame.mixer.Sound("chord_d.wav"),
    "A": pygame.mixer.Sound("chord_a.wav"),
    "E": pygame.mixer.Sound("chord_e.wav")
}

# Define chord zones (x1, y1, x2, y2)
zones = {
    "C": (50, 300, 150, 450),  # Left-most zone
    "G": (170, 300, 270, 450),
    "D": (290, 300, 390, 450),
    "A": (410, 300, 510, 450),
    "E": (530, 300, 630, 450)  # Right-most zone
}

# Colors for visual zones
zone_colors = {
    "C": (255, 255, 0),
    "G": (255, 0, 255),
    "D": (0, 255, 255),
    "A": (0, 128, 255),
    "E": (128, 255, 0)
}

# Webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw chord zones
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

            # Check if index finger is in any chord zone
            for zone, (x1, y1, x2, y2) in zones.items():
                if x1 < x < x2 and y1 < y < y2:
                    chords[zone].play()  # Play corresponding chord
                    cv2.circle(frame, (x, y), 15, (255, 255, 255), -1)  # Visual feedback

    # Display the frame
    cv2.imshow("Magical Guitar", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""


with open(MAGICAL_GUITAR_FILE, "w") as f:
    f.write(magical_guitar_code)

# Streamlit app
def main():
    st.title("Magical Music Instruments 🎶")
    st.write("Welcome to the Magical Instruments app! Choose your instrument below.")

    # Button to start drums
    if st.button("Play Drums"):
        st.write("Launching Magical Drums...")
        os.system(f"python {MAGICAL_DRUMS_FILE}")
        st.stop()  # Stop the Streamlit app execution

    # Button to start guitar
    if st.button("Play Guitar"):
        st.write("Launching Magical Guitar...")
        os.system(f"python {MAGICAL_GUITAR_FILE}")
        st.stop()  # Stop the Streamlit app execution

if __name__ == "__main__":
    main()