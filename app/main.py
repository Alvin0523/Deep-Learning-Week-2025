import streamlit as st
import torch
import cv2
import vision
import tele
import voice
import os
import time

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

admin = "Dana"
user = "Mommy"

# Streamlit App Title
st.title("YOLOv8 Live Object Detection")

# Sidebar Start Button
start_button = st.sidebar.button("Start Webcam")

# Sidebar Start Button
st.sidebar.title("🔧 Settings")
start_button = st.sidebar.button("Start Webcam")

# 1️⃣ Personal Information
full_name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, step=1)

# 2️⃣ Emergency Contact
st.sidebar.subheader("📞 Emergency Contact")
emergency_contact_name = st.sidebar.text_input("Contact Name")
emergency_contact_number = st.sidebar.text_input("Phone Number")

# 3️⃣ Medical Information
st.sidebar.subheader("⚕️ Medical Information")
blood_type = st.sidebar.selectbox("Blood Type", ["Unknown", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
medical_conditions = st.sidebar.text_area("Existing Medical Conditions (e.g., Diabetes, Hypertension)")
medications = st.sidebar.text_area("Current Medications (Name & Dosage)")
allergies = st.sidebar.text_area("Allergies (Medications, Food, Environmental)")
dnr_status = st.sidebar.radio("Do-Not-Resuscitate (DNR) Order", ["No", "Yes"])



def generate_emergency_message():
    return f"""
🚨 **EMERGENCY ALERT** 🚨

👤 **Patient:** {full_name} (Age: {age})
🩸 Blood Type: {blood_type}
⚕️ Medical Conditions: {medical_conditions if medical_conditions else 'None'}
💊 Medications: {medications if medications else 'None'}
🚨 Allergies: {allergies if allergies else 'None'}
📜 DNR Status: {dnr_status}
🦽

📞 Emergency Contact: {emergency_contact_name} ({emergency_contact_number})

🆘 Immediate action may be required!
"""

# Video frame placeholder

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
                tele.send_telegram_alert(user, f"{user} says {result}")
                message_2.success(f"I will inform {admin} and ask for help")

            # Case 2: User is okay
            elif "i am okay" in result.lower():
                tele.send_telegram_alert(user, f"{user} says {result}")
                message_2.success(f"I will inform {admin} and standby")

            else:
                message_2.success("Be careful")

            # **WAIT 5 SECONDS THEN CLEAR MESSAGES**
            time.sleep(5)
            message_1.empty()
            message_2.empty()

        else:
            message_1.empty()  # Clear the placeholder if no object is detected

    cap.release()
    st.sidebar.write("Webcam stopped.")
