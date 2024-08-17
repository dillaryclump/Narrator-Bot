Narrator Bot
By Dillon Bishop

you need anthropic and elevenlabs api keys to run this program

1. Clone this repository
2. Create a `.env` file in the root directory with the following content:
-ANTHROPIC_API_KEY=*your api key here*
-ELEVEN_LABS_API_KEY=*your api key here*
3. Replace `your_replicate_api_token`, `your_anthropic_api_key`, and `your_eleven_labs_api_key` with your actual API keys.
4. Install the required dependencies: `pip install -r requirements.txt`
5. Run the script: `python your_script_name.py`

notes:
you can change the voice by changing this line of code in main.py in generate_speech():
voice_id="N2lVS1w4EtoT3dr4eOWO"

you can change how often it runs by changing this line in the main loop the normal is 60 seconds but its a bit expensive:
time.sleep(60)  # Wait for 1 minute before the next capture

you can change the bots personality by changing this code here:
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

this was made in visual studio code on a windows 11 computer:
Edition	Windows 11 Home
Version	23H2
OS build	22631.4037

use cases:
as a prank
to keep yourself entertained at work
perhaps some sort of weird AI companion in the future