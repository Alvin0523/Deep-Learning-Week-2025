import pyttsx3

def tts_init(): 
    engine = pyttsx3.init()
    #text to speech settings
    engine.setProperty('rate', 100)     # Speed percent (can go over 100)
    engine.setProperty('volume', 1.0)  # Volume 0-1
    return engine
