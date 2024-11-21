import os
import sys
from dotenv import load_dotenv
from PIL import Image
import io
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.vision_service import VisionService
from backend.translator_service import TranslatorService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_vision_and_translation():
    # Load environment variables
    load_dotenv()
    
    # Initialize services
    try:
        vision_service = VisionService()
        translator_service = TranslatorService()
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
        
        # Extract text
        logger.info("Extracting text from image...")
        extracted_text = vision_service.extract_text(image_stream)
        
        if not extracted_text:
            logger.error("No text was extracted from the image")
            return
            
        print("\nExtracted Text:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)
        
        # Define target languages for translation
        target_languages = {
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Arabic': 'ar'
        }
        
        # Translate to each target language
        for language_name, language_code in target_languages.items():
            print(f"\nTranslating to {language_name}...")
            translated_text = translator_service.translate_text(
                extracted_text,
                language_code
            )
            
            if translated_text:
                print(f"\n{language_name} Translation:")
                print("-" * 50)
                print(translated_text)
                print("-" * 50)
            else:
                logger.error(f"Translation to {language_name} failed")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_vision_and_translation()