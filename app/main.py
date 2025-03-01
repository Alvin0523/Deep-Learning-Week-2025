import streamlit as st
import torch
import cv2
import vision
import tele
import voice
import os
import time
import sms
from Pages import Settings


torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

# Streamlit App Title
st.title("Safe Vision")

# Sidebar Start Button
st.sidebar.title("🔧 Settings")
start_button = st.sidebar.button("Start Webcam")

# Video frame placeholder
frame_placeholder = st.empty()

# Detection placeholder (for activating something)
message_1 = st.empty()
message_2 = st.empty()

if start_button:

    st.sidebar.write("Webcam feed started. Press 'Stop' to exit.")

    # Open webcam once (Avoid reinitializing in every frame)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.sidebar.error("Error: Could not open webcam.")
        st.stop()

    # Sidebar Stop Button
    stop_button = st.sidebar.button("Stop")

    while not stop_button:
        frame = vision.get_frame(cap)  # Get processed frame from vision module

        if frame is None:
            st.warning("Failed to retrieve frame.")
            break

        # Check for object detection
        detected = vision.is_object_detected(frame)

        # Show frame in Streamlit
        frame_placeholder.image(frame, channels="RGB", use_container_width=True)

        # Activate something when an object is detected
        if detected:
            message_1.success("🚨 Fall Detected!")
            time.sleep(0.5)
            
            # Ask the user if they are okay using text-to-speech
            voice.say("Hello, Are you okay?")
            message_2.success("Hello, Are you okay?")
            time.sleep(3.0)
            
            message_2.success("Listening...")
            time.sleep(0.5)
            result = voice.mic.listen()

            # Case 1: User needs help
            if "help" in result.lower():
                tele.send_telegram_alert(f"{Settings.full_name} says {Settings.result}")
                message_2.success(f"I will inform {Settings.emergency_contact_name} and ask for help")

            # Case 2: User is okay
            elif "okay" in result.lower():
                tele.send_telegram_alert(f"{Settings.full_name} says {Settings.result}")
                message_2.success(f"I will inform {Settings.emergency_contact_name} and standby")

            else:
                message_2.success("No valid response detected. Waiting 10 seconds before calling an ambulance...")
                time.sleep(10)  # Wait for 10 seconds
                sms.emergency(e_message)

        # **WAIT 5 SECONDS THEN CLEAR MESSAGES**
        time.sleep(5)
        message_1.empty()
        message_2.empty()

    cap.release()
    st.sidebar.write("Webcam stopped.")
