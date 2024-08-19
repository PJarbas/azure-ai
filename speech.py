import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
 
load_dotenv()


class TextSpeech:
    def __init__(self, recognition_language='pt-BR',
                synthesis_voice_name='pt-BR-GiovannaNeural') -> None:
        """
        Text to speech module using Azure speechsdk
        Args:
            recognition_language (str): Idiom of the voice.
            synthesis_voice_name (str): Name of the voice.
        """
        
        self.recognition_language = recognition_language
        self.synthesis_voice_name = synthesis_voice_name
        
        self.config_speech()
        self.config_speech_recognizer()
        self.config_speech_synthesizer()

    def config_speech(self):
        """
        API Configurations with key and region.
        """

        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get('SPEECH_KEY'),
            region=os.environ.get('SPEECH_REGION'))

    def config_speech_recognizer(self):
        """
        set the configurations of the recognizer
        https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt
            
        """

        self.speech_config.speech_recognition_language = self.recognition_language

        microphone_audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=microphone_audio_config
        )

    def config_speech_synthesizer(self):
        """
        set the configurations of the synthesier.
        https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts
        """

        self.speech_config.speech_synthesis_voice_name = self.synthesis_voice_name
    
        speaker_audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=speaker_audio_config
        )
    
    def run(self):

        # Get text from the console and synthesize to the default speaker.
        print("Enter some text that you want to speak >")
        text = input()

        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))

        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details

            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
            
                if cancellation_details.error_details:
            
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

if __name__=="__main__":
    speech = TextSpeech(
        recognition_language='pt-BR',
        synthesis_voice_name='pt-BR-GiovannaNeural'
    )
    speech.run()