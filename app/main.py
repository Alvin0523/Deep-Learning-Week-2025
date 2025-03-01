import streamlit as st
import cv2
import vision
import tele
import whisper

admin = "Dana"
user = "Mommy"

# Streamlit App Title
st.title("YOLOv8 Live Object Detection")

# Sidebar Start Button
start_button = st.sidebar.button("Start Webcam")

# Video frame placeholder
frame_placeholder = st.empty()

# Detection placeholder (for activating something)
detection_placeholder = st.empty()

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
            detection_placeholder.success("🚨 Object Detected!")
            # asked the user if they are okay using text to speech
            whisper.say("Hello, Are you okay?")
            whisper.run()
            result = whisper.listen
            print(f"You said: {result}")
            
            # case 1: user is not okay -  help needed
            if "help" in result.lower():
                whisper.say(f"I will inform {admin}, and ask for help")
                whisper.run
                tele.send_telegram_alert(user,f"{user} says {result}")
                # insert the string matching to call for help
            
            # case 2: user is okay - no help needed
            elif "i am okay" in result.lower():
                whisper.say(f"I will inform {admin}, and standby")
                whisper.runAndWait()
                tele.send_telegram_alert(user,f"{user} says {result}")
                # insert the string matching to standby

            else: 
                whisper.say(f"Be careful")
                   
        else:
            detection_placeholder.empty()  # Clear the placeholder if no object is detected
            
    cap.release()
    st.sidebar.write("Webcam stopped.")
