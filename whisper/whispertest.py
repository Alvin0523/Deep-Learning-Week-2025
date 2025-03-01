from whisper_mic import WhisperMic
import sys

def main():
    # Initialize WhisperMic with your desired settings
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

    print("Speak 'stop' to exit. Listening...")

    try:
        while True:
            result = mic.listen()
            print(f"You said: {result}")

            # Check for a stop phrase
            if "stop" in result.lower():
                print("Stopping the loop because you said 'stop'.")
                break

            # Check for a specific trigger phrase
            if "my trigger phrase" in result.lower():
                print("Trigger phrase detected! Taking action...")
                # Insert the action you want to perform here

    except KeyboardInterrupt:
        print("Operation interrupted by user (Ctrl+C).")

    finally:
        # If you're saving audio to a file, close it here
        # if mic.file is open:
        #     mic.file.close()
        pass

if __name__ == "__main__":
    main()
