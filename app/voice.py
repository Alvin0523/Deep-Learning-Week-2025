import pyttsx3
from whisper_mic import WhisperMic

# Initialize WhisperMic with desired settings
mic = WhisperMic(
        model="tiny",
        english=True,
        verbose=False,
        energy=100,
        pause=0.8,
        dynamic_energy=False,
        save_file=False,
        device="cuda",   # or "cpu"/"mps" if that's what you want
        mic_index=None,
        implementation="whisper",
        hallucinate_threshold=400
    )

#init the text to speech engine
engine = pyttsx3.init()

#text to speech settings
engine.setProperty('rate', 100)     # Speed percent (can go over 100)
engine.setProperty('volume', 1.0)  # Volume 0-1

def say(message):
    engine.say(message)

def run():
    engine.stop()  # Ensure previous speech is stopped
    print("stop")
    engine.runAndWait()

def listen():
    mic.listen()