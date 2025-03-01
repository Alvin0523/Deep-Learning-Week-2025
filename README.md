# Deep-Learning-Week-2025 (Mitsuru)

# SafeVision

An AI-powered web application that detects human collapses and triggers immediate, automated emergency responses. SafeVision leverages computer vision for real-time fall detection, natural language processing for user verification, and automated alerts via Telegram/SMS with attached vital information—drastically reducing the response time for life-threatening emergencies.

## Table of Contents
1. [Introduction](#introduction)  
2. [Key Features](#key-features)  
3. [How It Works](#how-it-works)   
4. [Limitations & Future Plans](#limitations--future-plans)  
5. [Technology Stack](#technology-stack)  
6. [How to Run](#how-to-run)   

---

## Introduction
Falls are a leading cause of injury and mortality among the elderly. In Singapore alone, **40% of injury-related deaths** for seniors result from falls, and **one-third of individuals aged 65+** experience at least one fall per year. Delayed detection of collapses—such as heart attacks or strokes—worsens patient outcomes, as each additional minute without assistance increases the risk of severe complications or death.

Traditional monitoring solutions (e.g., wearables) can fail if forgotten or not worn. **SafeVision** addresses this gap by providing around-the-clock, automated monitoring and immediate emergency contact, thereby minimizing critical delays and preventing preventable fatalities.

---

## Key Features
1. **Real-Time Fall Detection**  
   - Utilizes computer vision models to identify human falls instantly through a connected camera feed.

2. **Voice-Enabled Response**  
   - Employs NLP to generate voice prompts when a fall is detected. The system asks questions like “Are you okay?” and listens for responses.

3. **Automated Emergency Actions**  
   - If there is no response for 30 seconds or if the user verbally requests help, SafeVision dispatches alerts to emergency services and designated contacts.

4. **Vital Sign Integration**  
   - Optionally pairs with wearable devices (e.g., Fitbit) to gather real-time heart rate and other vitals for more comprehensive emergency information.

5. **Incident Reporting**  
   - Sends notifications via Telegram or SMS with crucial data: incident time, location snapshots, and patient’s latest vitals. Medical teams can react quickly with preliminary insights.

6. **Multi-Scenario Handling**  
   - Responsive to various outcomes:
     - **No Response**: Automatically calls for emergency services after 30 seconds.
     - **Help Requested**: Immediately dispatches emergency alerts.
     - **False Alarm**: If user says “I’m okay,” the system cancels emergency actions.

---

## How It Works
1. **Video Stream Analysis**  
   - A camera continuously monitors a space (home, nursing facility, etc.).
   - Our AI-based fall-detection model runs in real time.

2. **Natural Language Processing & Automated Prompts**  
   - On detecting a fall, SafeVision generates an audio prompt to check on the individual.
   - The system records and interprets any spoken response via built-in NLP.

3. **Emergency Decision Logic**  
   - **No Response / “Help!”**: Notifies designated contacts and/or emergency services immediately.
   - **All Clear**: No further action taken, system resets monitoring.

4. **Alerts & Reporting**  
   - SafeVision automatically compiles:
     - Image snapshot from camera
     - Timestamp of incident
     - (Optional) Wearable device vitals
   - Sends this bundle to next-of-kin via Telegram and triggers an SMS to emergency responders if necessary.


## Technology Stack
- **Computer Vision**: YOLOV11 Model (Ultralytics)
- **NLP**: Whisper-mic (OpenAI), Pyttsx (text-to-speech)
- **Frontend**: Streamlit
- **Integration**: Fitbit
- **Messaging**: Telegram Bot API, Twilio

---

**Thank you for your interest in SafeVision!**  
Together, let’s create a safer environment for everyone by leveraging proactive, AI-driven medical intervention.
