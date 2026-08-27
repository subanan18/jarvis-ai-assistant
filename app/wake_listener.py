import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from openwakeword.model import Model


PROJECT_FOLDER = Path(__file__).resolve().parent
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280
WAKE_THRESHOLD = 0.50


def start_jarvis() -> None:
    """Start the LiveKit JARVIS agent and wait until the session closes."""
    agent_file = PROJECT_FOLDER / "agent.py"

    if not agent_file.exists():
        print(f"Error: agent.py was not found at {agent_file}")
        return

    print("\nStarting Jarvis...\n")

    try:
        subprocess.run(
            [sys.executable, str(agent_file), "console"],
            cwd=PROJECT_FOLDER.parent,
            check=False,
        )
    except OSError as error:
        print(f"Could not start Jarvis: {error}")


def listen_for_wake_word() -> bool:
    """Listen continuously for the phrase 'Hey Jarvis'."""
    print("Loading the Hey Jarvis wake-word model...")

    try:
        wake_model = Model(inference_framework="onnx")
    except Exception as error:
        print(f"Could not load the wake-word model: {error}")
        return False

    available_models = list(wake_model.models.keys())
    jarvis_models = [
        model_name
        for model_name in available_models
        if "jarvis" in model_name.lower()
    ]

    if not jarvis_models:
        print(
            "\nThe Hey Jarvis model was not found.\n"
            "Run: python scripts/download_wake_models.py"
        )
        return False

    print("\nJarvis is sleeping.")
    print('Say: "Hey Jarvis"')
    print("Press Ctrl+C to stop.\n")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=CHUNK_SIZE,
        ) as microphone:
            while True:
                audio_data, overflowed = microphone.read(CHUNK_SIZE)

                if overflowed:
                    print("Microphone audio overflow detected.")

                audio_frame = np.asarray(audio_data, dtype=np.int16).flatten()
                predictions = wake_model.predict(audio_frame)

                for model_name, score in predictions.items():
                    if "jarvis" not in model_name.lower():
                        continue

                    if score >= WAKE_THRESHOLD:
                        print(
                            f'\nWake word detected: "{model_name}" '
                            f"(confidence: {score:.2f})"
                        )
                        print("Waking up Jarvis...")
                        return True

    except KeyboardInterrupt:
        print("\nWake listener stopped.")
        return False
    except sd.PortAudioError as error:
        print(f"\nMicrophone error: {error}")
        print("Check Windows microphone permissions and your default microphone.")
        return False
    except Exception as error:
        print(f"\nWake listener error: {error}")
        return False


def main() -> None:
    """Keep listening and restart wake mode after the agent closes."""
    print("=" * 45)
    print("Jarvis Wake Listener")
    print("=" * 45)

    while True:
        wake_detected = listen_for_wake_word()
        if not wake_detected:
            break

        start_jarvis()
        print("\nJarvis has closed.")
        print("Returning to wake-word mode...\n")
        time.sleep(2)


if __name__ == "__main__":
    main()
