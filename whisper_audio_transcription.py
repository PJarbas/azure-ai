import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


class AudioTranscriber:
    def __init__(self, model="whisper"):
        self.model = model

    def get_client(self):

        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version=os.getenv("API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        return client
    
    def transcribe_audio(self, audio_file_path):

        client = self.get_client()

        try:
            with open(audio_file_path, "rb") as audio_file:

                response = client.audio.transcriptions.create(
                    file=audio_file,            
                    model=self.model
                )

                print(response)

                return response.text
        except Exception as e:
            print(f"Error to transcribe audio: {e}")
            return None

if __name__ == "__main__":
    
    audio_file_path = 'audio.wav'
    
    transcriber = AudioTranscriber()
    transcription = transcriber.transcribe_audio(audio_file_path)
    
    if transcription:
        print("Result:")
        print(transcription)