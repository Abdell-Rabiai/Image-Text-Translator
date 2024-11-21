import os
import azure.cognitiveservices.speech as speechsdk
import logging
from typing import Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        """Initialize the Speech Service with Azure credentials."""
        try:
            self.key = os.getenv('AZURE_SPEECH_KEY')
            self.region = os.getenv('AZURE_SPEECH_REGION')
            
            if not self.key or not self.region:
                raise ValueError("Azure Speech credentials not found in environment variables")
            
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.key,
                region=self.region
            )
            # Set default output format
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
            )
            logger.info("Speech Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Speech Service: {str(e)}")
            raise

    def text_to_speech(self, text: str, language: str = "en-US") -> Optional[bytes]:
        """
        Convert text to speech using default voice for the language.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., "en-US", "es-ES")
            
        Returns:
            bytes: Audio data or None if synthesis failed
        """
        try:
            # Create output file name
            output_file = f"temp_speech_{int(time.time())}.wav"
            
            # Configure speech synthesizer
            self.speech_config.speech_synthesis_language = language
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Simple synthesis without SSML
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Read the audio file
                with open(output_file, "rb") as audio_file:
                    audio_data = audio_file.read()
                logger.info(f"Text-to-speech conversion successful for language: {language}")
                return audio_data
            else:
                error_details = f"Speech synthesis failed with reason: {result.reason}"
                logger.error(error_details)
                return None

        except Exception as e:
            logger.error(f"Text-to-speech conversion failed: {str(e)}")
            return None
            
        finally:
            # Clean up the temporary file
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file: {str(e)}")

    def text_to_speech_with_voice(self, text: str, voice_name: str) -> Optional[bytes]:
        """
        Convert text to speech using a specific voice.
        
        Args:
            text: Text to convert to speech
            voice_name: Name of the voice to use
            
        Returns:
            bytes: Audio data or None if synthesis failed
        """
        try:
            # Create output file name
            output_file = f"temp_speech_{int(time.time())}.wav"
            
            # Configure speech synthesizer
            self.speech_config.speech_synthesis_voice_name = voice_name
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Synthesize text to speech
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Read the audio file
                with open(output_file, "rb") as audio_file:
                    audio_data = audio_file.read()
                logger.info(f"Text-to-speech conversion successful using voice: {voice_name}")
                return audio_data
            else:
                error_details = f"Speech synthesis failed with reason: {result.reason}"
                logger.error(error_details)
                return None

        except Exception as e:
            logger.error(f"Text-to-speech conversion failed: {str(e)}")
            return None
            
        finally:
            # Clean up the temporary file
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file: {str(e)}")

    def verify_service(self) -> bool:
        """
        Verify that the speech service is working correctly.
        
        Returns:
            bool: True if service is working, False otherwise
        """
        try:
            test_text = "Testing speech service."
            result = self.text_to_speech(test_text, "en-US")
            return result is not None
        except Exception as e:
            logger.error(f"Service verification failed: {str(e)}")
            return False