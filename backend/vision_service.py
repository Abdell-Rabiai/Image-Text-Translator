# this is for
# extract text from images using the Computer Vision OCR API.import os
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
from typing import Optional, IO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisionService:
    def __init__(self):
        """Initialize the Vision Service with Azure credentials."""
        try:
            self.endpoint = os.getenv('AZURE_VISION_ENDPOINT')
            self.key = os.getenv('AZURE_VISION_KEY')
            
            if not self.endpoint or not self.key:
                raise ValueError("Azure Vision credentials not found in environment variables")
            
            self.client = ComputerVisionClient(
                endpoint=self.endpoint,
                credentials=CognitiveServicesCredentials(self.key)
            )
            logger.info("Vision Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Vision Service: {str(e)}")
            raise

    def extract_text(self, image_data: IO) -> Optional[str]:
        """
        Extract text from an image using Azure's OCR service.
        
        Args:
            image_data: File-like object containing the image data
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            # Start the async OCR operation
            read_response = self.client.read_in_stream(image_data, raw=True)
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Wait for the operation to complete
            max_retries = 10
            retry_delay = 1
            current_try = 0
            
            while current_try < max_retries:
                result = self.client.get_read_result(operation_id)
                if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                    break
                time.sleep(retry_delay)
                current_try += 1

            # Extract and return the text
            if result.status == OperationStatusCodes.succeeded:
                text = ""
                for text_result in result.analyze_result.read_results:
                    for line in text_result.lines:
                        text += line.text + "\n"
                logger.info("Text extracted successfully")
                return text.strip()
            else:
                logger.warning(f"Text extraction failed with status: {result.status}")
                return None

        except Exception as e:
            logger.error(f"Error in text extraction: {str(e)}")
            return None

    def is_valid_image(self, image_data: IO) -> bool:
        """
        Validate if the provided image data is suitable for OCR.
        
        Args:
            image_data: File-like object containing the image data
            
        Returns:
            bool: True if image is valid, False otherwise
        """
        try:
            # Try to analyze the image
            image_analysis = self.client.analyze_image_in_stream(
                image_data,
                visual_features=['Objects', 'Tags']
            )
            return True
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            return False