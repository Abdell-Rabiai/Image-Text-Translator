import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import requests
import azure.cognitiveservices.speech as speechsdk

def test_azure_services():
    # Load environment variables
    load_dotenv()
    
    print("Testing Azure services connection...\n")
    
    # Test Computer Vision
    try:
        vision_client = ComputerVisionClient(
            endpoint=os.getenv('AZURE_VISION_ENDPOINT'),
            credentials=CognitiveServicesCredentials(os.getenv('AZURE_VISION_KEY'))
        )
        print("✓ Computer Vision credentials verified")
    except Exception as e:
        print(f"✗ Computer Vision error: {str(e)}")
    
    # Test Translator
    try:
        # Test translation with a simple API call
        translator_endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')
        path = '/translate'
        constructed_url = translator_endpoint + path
        
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': 'es'
        }
        
        headers = {
            'Ocp-Apim-Subscription-Key': os.getenv('AZURE_TRANSLATOR_KEY'),
            'Ocp-Apim-Subscription-Region': os.getenv('AZURE_TRANSLATOR_REGION'),
            'Content-type': 'application/json'
        }
        
        body = [{
            'text': 'Hello, world!'
        }]
        
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("✓ Translator credentials verified")
    except Exception as e:
        print(f"✗ Translator error: {str(e)}")
    
    # Test Speech Services
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('AZURE_SPEECH_KEY'),
            region=os.getenv('AZURE_SPEECH_REGION')
        )
        print("✓ Speech Services credentials verified")
    except Exception as e:
        print(f"✗ Speech Services error: {str(e)}")

if __name__ == "__main__":
    test_azure_services()