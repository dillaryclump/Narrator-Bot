import os
import time
import anthropic
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import base64
import pyautogui
import wave
import pyaudio
import io

# Load environment variables
load_dotenv()

# Initialize APIs
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
eleven_labs_client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))


def play_audio(audio_data):
    try:
        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=22050,
                        output=True)

        # Play stream
        for chunk in audio_data:
            stream.write(chunk)

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()

        print("Audio played successfully")
    except Exception as e:
        print(f"Error playing audio: {e}")

def capture_screenshot():
    print("Capturing screenshot...")
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("captured_screenshot.png")
        print("Screenshot captured successfully")
        return "captured_screenshot.png"
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def analyze_image(image_path):
    if image_path is None or not os.path.exists(image_path):
        return "I couldn't capture a screenshot. Is your screen invisible?"
    
    print(f"Analyzing screenshot: {image_path}")
    with open(image_path, "rb") as image_file:
        try:
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64.b64encode(image_file.read()).decode()
                                }
                            },
                            {
                                "type": "text",
                                "text": "Provide a brief, snarky comment about what you see."
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error analyzing screenshot: {e}")
            return "I'm having trouble being snarky about your screen right now. Must be too boring to comment on."

def generate_speech(text):
    print(f"Generating speech for: {text}")
    try:
        audio_generator = eleven_labs_client.text_to_speech.convert(
            voice_id="N2lVS1w4EtoT3dr4eOWO",
            output_format="pcm_16000",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            ),
        )
        
        play_audio(audio_generator)
    except Exception as e:
        print(f"Error generating or playing speech: {e}")

def main():
    while True:
        try:
            image_path = capture_screenshot()
            comment = analyze_image(image_path)
            print(f"Generated comment: {comment}")
            generate_speech(comment)
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
        
        print("Waiting for 60 seconds before next iteration...")
        time.sleep(60)  # Wait for 1 minute before the next capture

if __name__ == "__main__":
    main()