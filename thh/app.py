import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pygame
from PIL import Image

# Initialize MediaPipe and drawing settings
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame for sound mixing
# pygame.mixer.init()
pygame.init()
drum_sounds = {
    "bass": pygame.mixer.Sound("bass_drum.wav"),
    "snare": pygame.mixer.Sound("snare_drum.wav"),
    "cymbal": pygame.mixer.Sound("cymbal.wav")
}

guitar_sounds = {
    "C": pygame.mixer.Sound("chord_c.wav"),
    "G": pygame.mixer.Sound("chord_g.wav"),
    "D": pygame.mixer.Sound("chord_d.wav"),
    "A": pygame.mixer.Sound("chord_a.wav"),
    "E": pygame.mixer.Sound("chord_e.wav")
}

# Zones for touching
drum_zones = {
    "bass": (50, 300, 200, 450),
    "snare": (250, 300, 400, 450),
    "cymbal": (450, 300, 600, 450)
}

guitar_zones = {
    "C": (50, 300, 150, 450),
    "G": (170, 300, 270, 450),
    "D": (290, 300, 390, 450),
    "A": (410, 300, 510, 450),
    "E": (530, 300, 630, 450)
}

# Webcam feed processing with opencv
def process_webcam(zones, sounds, zone_colors, title):
    st.title(title)
    run = st.checkbox("Start Webcam")

    if run:
        cap = cv2.VideoCapture(0)

        stframe = st.empty()  

        while run:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            
            for zone, (x1, y1, x2, y2) in zones.items():
                cv2.rectangle(frame, (x1, y1), (x2, y2), zone_colors[zone], 2)
                cv2.putText(frame, zone, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, zone_colors[zone], 2)

            # Detect hands (21marking)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get coordinates of the tip of the index finger, 8th marking
                    index_finger_tip = hand_landmarks.landmark[8]
                    x, y = int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0])

                    # Check for detection
                    for zone, (x1, y1, x2, y2) in zones.items():
                        if x1 < x < x2 and y1 < y < y2:
                            sounds[zone].play()  #play sounds
                            cv2.circle(frame, (x, y), 15, (255, 255, 255), -1)   #white dotted markings

            
            stframe.image(frame, channels="BGR", use_column_width=True)

        cap.release()
    else:
        st.write("Click the checkbox to start the webcam!")

# Streamlit ui
def main():
    st.title("Magical Music Instruments 🎶")
    st.write("Welcome to the Magical Instruments app! Choose your instrument below.")

    choice = st.radio("Select an instrument:", ["Drums", "Guitar"])

    if choice == "Drums":
        process_webcam(
            zones=drum_zones,
            sounds=drum_sounds,
            zone_colors={"bass": (0, 255, 0), "snare": (255, 0, 0), "cymbal": (0, 0, 255)},
            title="Magical Drums &",
        )
    elif choice == "Guitar":
        process_webcam(
            zones=guitar_zones,
            sounds=guitar_sounds,
            zone_colors={
                "C": (255, 255, 0),
                "G": (255, 0, 255),
                "D": (0, 255, 255),
                "A": (0, 128, 255),
                "E": (128, 255, 0),
            },
            title="Magical Guitar* ",
        )

if __name__ == "__main__":
    main()
