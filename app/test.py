import pyttsx3

engine = pyttsx3.init()

# Text-to-speech settings
engine.setProperty('rate', 100)  # Speed percent (can go over 100)
engine.setProperty('volume', 1.0)  # Volume 0-1

def say(message):
    engine.say(message)
    print(f"Queued message: {message}")  # Debugging print

def run():
    print("Running TTS engine...")  # Debugging print
    engine.runAndWait()
    print("TTS finished.")  # Debugging print

say("Hello, Are you okay?")
run()
