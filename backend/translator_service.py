import os
import requests
import logging
from typing import Optional, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslatorService:
    def __init__(self):
        """Initialize the Translator Service with Azure credentials."""
        try:
            self.key = os.getenv('AZURE_TRANSLATOR_KEY')
            self.region = os.getenv('AZURE_TRANSLATOR_REGION')
            self.endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 
                                    'https://api.cognitive.microsofttranslator.com')
            
            if not self.key or not self.region:
                raise ValueError("Azure Translator credentials not found in environment variables")
            
            logger.info("Translator Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Translator Service: {str(e)}")
            raise

    def translate_text(self, text: str, target_language: str, 
                    source_language: Optional[str] = None) -> Optional[str]:
        """
        Translate text to the target language.
        
        Args:
            text: Text to translate
            target_language: Language code to translate to (e.g., 'es' for Spanish)
            source_language: Optional source language code
            
        Returns:
            str: Translated text or None if translation failed
        """
        try:
            path = '/translate'
            constructed_url = self.endpoint + path

            params = {
                'api-version': '3.0',
                'to': target_language
            }
            
            if source_language:
                params['from'] = source_language

            headers = {
                'Ocp-Apim-Subscription-Key': self.key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json'
            }

            body = [{
                'text': text
            }]

            logger.info(f"Sending translation request for text: {text[:50]}...")
            response = requests.post(constructed_url, params=params, 
                                headers=headers, json=body)
            response.raise_for_status()

            translations = response.json()
            translated_text = translations[0]["translations"][0]["text"]
            logger.info(f"Text translated successfully to {target_language}")
            return translated_text

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {http_err.response.content}")
            return None
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return None

    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """
        Get list of supported languages for translation.
        
        Returns:
            Dict containing language codes and names
        """
        try:
            path = '/languages'
            constructed_url = self.endpoint + path

            params = {
                'api-version': '3.0',
                'scope': 'translation'
            }

            response = requests.get(constructed_url, params=params)
            response.raise_for_status()

            languages = response.json()
            return languages['translation']

        except Exception as e:
            logger.error(f"Failed to get available languages: {str(e)}")
            return {}