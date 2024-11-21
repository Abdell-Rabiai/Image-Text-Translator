import os
import sys
from dotenv import load_dotenv
from PIL import Image
import io
import logging
import time

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.vision_service import VisionService
from backend.translator_service import TranslatorService
from backend.speech_service import SpeechService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Language configurations with their voice names
LANGUAGE_CONFIG = {
    'English': {
        'code': 'en',
        'voice': 'en-US-JennyMultilingualNeural',
        'speech_code': 'en-US'
    },
    'Spanish': {
        'code': 'es',
        'voice': 'es-ES-ElviraNeural',
        'speech_code': 'es-ES'
    },
    'French': {
        'code': 'fr',
        'voice': 'fr-FR-DeniseNeural',
        'speech_code': 'fr-FR'
    },
    'Arabic': {
        'code': 'ar',
        'voice': 'ar-SA-ZariyahNeural',
        'speech_code': 'ar-SA'
    }
}

def save_audio(audio_data: bytes, filename: str):
    """Save audio data to a file"""
    os.makedirs('output/audio', exist_ok=True)
    filepath = os.path.join('output/audio', filename)
    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio_data)
    return filepath

def test_all_services():
    # Load environment variables
    load_dotenv()
    
    # Initialize services
    try:
        vision_service = VisionService()
        translator_service = TranslatorService()
        speech_service = SpeechService()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        return

    # Image path
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "images", "poet.jpg")
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found at {image_path}")
            return
            
        # Read and process image
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        image_stream = io.BytesIO(image_data)
        
        # Step 1: Extract text
        logger.info("Extracting text from image...")
        extracted_text = vision_service.extract_text(image_stream)
        
        if not extracted_text:
            logger.error("No text was extracted from the image")
            return
            
        print("\nExtracted Text:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)
        
        # Generate speech for original text
        logger.info("Generating speech for original text...")
        
        original_audio = speech_service.text_to_speech_with_voice(
            extracted_text,
            LANGUAGE_CONFIG['English']['voice']
        )
        
        if original_audio:
            original_audio_path = save_audio(original_audio, 'original_speech.wav')
            print(f"Original speech saved to: {original_audio_path}")
        
        # Step 2 & 3: Translate text and generate speech for each language
        for language_name, config in LANGUAGE_CONFIG.items():
            if language_name == 'English':  # Skip English as it's our source
                continue
                
            print(f"\nProcessing {language_name}...")
            
            # Translate
            translated_text = translator_service.translate_text(
                extracted_text,
                config['code']
            )
            
            if translated_text:
                print(f"\n{language_name} Translation:")
                print("-" * 50)
                print(translated_text)
                print("-" * 50)
                
                # Generate speech
                logger.info(f"Generating speech for {language_name} translation...")
                audio_data = speech_service.text_to_speech_with_voice(
                    translated_text,
                    config['voice']
                )
                
                if audio_data:
                    audio_path = save_audio(audio_data, f'{language_name.lower()}_speech.wav')
                    print(f"{language_name} speech saved to: {audio_path}")
                else:
                    logger.error(f"Speech generation failed for {language_name}")
            else:
                logger.error(f"Translation to {language_name} failed")
                
            # Add a small delay between API calls
            time.sleep(1)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise

def list_available_voices():
    """List all available voices for each language"""
    try:
        load_dotenv()
        speech_service = SpeechService()
        
        print("\nAvailable Voices:")
        print("-" * 50)
        
        for language_name, config in LANGUAGE_CONFIG.items():
            voices = speech_service.get_available_voices(config['speech_code'])
            print(f"\n{language_name} Voices:")
            for voice in voices:
                print(f"- {voice['name']} ({voice['gender']})")
                
    except Exception as e:
        logger.error(f"Error listing voices: {str(e)}")

if __name__ == "__main__":
    # Uncomment to list available voices
    # list_available_voices()
    
    test_all_services()