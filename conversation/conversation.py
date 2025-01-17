import subprocess
from openai import OpenAI
import time

client = OpenAI(api_key="YOUR_API_KEY")

for i in range(5):
#     subprocess.run(['bash', 'get_query.sh'])
#     audio_file = open("recorded_audio.wav", "rb")
#     transcript = client.audio.transcriptions.create(
#     model="whisper-1",
#     file=audio_file
#     # input="Hey there, how are you doing?"
# )
    
#     print(transcript.text)

    # 2. Then convert the transcribed text back to speech
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # You can choose different voices like "echo", "fable", "onyx", "nova", "shimmer"
        input="hello" #transcript.text
    )

    # 3. Save the audio response
    speech_response.stream_to_file("response.mp3")
    # with open("response.wav", "wb") as file:
    #     file.write(speech_response.content)
    # subprocess.run(['bash', 'talk.sh'])
    time.sleep(5)
