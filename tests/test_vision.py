import sys
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Add the parent directory to the Python path so we can import our backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.vision_service import VisionService

def test_image_extraction():
    # Load environment variables
    load_dotenv()
    
    # Initialize the Vision Service
    vision_service = VisionService()
    
    # Path to your image
    image_path = "images/poet.jpg"
    
    try:
        # Open and read the image
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        # Create a BytesIO object
        image_stream = io.BytesIO(image_data)
        
        print("Extracting text from image...")
        # Extract text from the image
        extracted_text = vision_service.extract_text(image_stream)
        
        if extracted_text:
            print("\nExtracted Text:")
            print("-" * 50)
            print(extracted_text)
            print("-" * 50)
        else:
            print("No text was extracted from the image.")
            
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_image_extraction()
