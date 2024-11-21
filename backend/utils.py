import logging
from typing import Optional, Tuple
from PIL import Image
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_image(image_data: bytes) -> Tuple[bool, Optional[str]]:
    """
    Validate image data and format.
    
    Args:
        image_data: Raw image data
        
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    try:
        # Try to open the image with PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Check image format
        if image.format not in ['JPEG', 'PNG', 'BMP']:
            return False, "Unsupported image format. Please use JPEG, PNG, or BMP."
        
        # Check image size
        max_size = 4 * 1024 * 1024  # 4MB
        if len(image_data) > max_size:
            return False, "Image size too large. Maximum size is 4MB."
        
        # Check dimensions
        max_dimension = 4096
        if image.width > max_dimension or image.height > max_dimension:
            return False, f"Image dimensions too large. Maximum dimension is {max_dimension}px."
        
        return True, None
        
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        return False, "Invalid image file."

def get_language_name(language_code: str, languages_dict: dict) -> str:
    """
    Get the display name for a language code.
    
    Args:
        language_code: ISO language code
        languages_dict: Dictionary of supported languages
        
    Returns:
        str: Display name of the language
    """
    try:
        return languages_dict[language_code]
    except KeyError:
        return "Unknown"