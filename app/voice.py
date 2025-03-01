import pyttsx3
import threading
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
    device="cuda",   # or "cpu"/"mps" if needed
    mic_index=None,
    implementation="whisper",
    hallucinate_threshold=400
)

# Lock to prevent multiple speech threads from running simultaneously
speech_lock = threading.Lock()

# Init the text-to-speech engine
engine = pyttsx3.init()

# Text-to-speech settings
engine.setProperty('rate', 100)  # Speed percent (can go over 100)
engine.setProperty('volume', 1.0)  # Volume 0-1

def say(message):
    """Runs speech in a separate thread to avoid blocking."""
    def speak():
        with speech_lock:
            engine.say(message)
            engine.runAndWait()  # This runs in the background

    threading.Thread(target=speak, daemon=True).start()

def listen():
    """Listens using WhisperMic while TTS is playing."""
    mic.listen()