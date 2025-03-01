import streamlit as st
import cv2
import vision

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
        else:
            detection_placeholder.empty()  # Clear the placeholder if no object is detected

    cap.release()
    st.sidebar.write("Webcam stopped.")
