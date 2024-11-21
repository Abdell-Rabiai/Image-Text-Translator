import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io
import time
from backend.vision_service import VisionService
from backend.translator_service import TranslatorService
from backend.speech_service import SpeechService

# Load environment variables
load_dotenv()

# Initialize services
@st.cache_resource
def init_services():
    vision_service = VisionService()
    translator_service = TranslatorService()
    speech_service = SpeechService()
    return vision_service, translator_service, speech_service

# Language configurations
LANGUAGES = {
    'English': {'code': 'en', 'voice': 'en-US-JennyMultilingualNeural', 'speech_code': 'en-US'},
    'Spanish': {'code': 'es', 'voice': 'es-ES-ElviraNeural', 'speech_code': 'es-ES'},
    'French': {'code': 'fr', 'voice': 'fr-FR-DeniseNeural', 'speech_code': 'fr-FR'},
    'Arabic': {'code': 'ar', 'voice': 'ar-SA-ZariyahNeural', 'speech_code': 'ar-SA'},
    'German': {'code': 'de', 'voice': 'de-DE-KatjaNeural', 'speech_code': 'de-DE'},
}

# Cache for storing audio data
if 'original_audio' not in st.session_state:
    st.session_state.original_audio = None
if 'translated_audio' not in st.session_state:
    st.session_state.translated_audio = None

def main():
    st.set_page_config(
        page_title="Image Text Translator",
        page_icon="🌍",
        layout="wide"
    )

    st.title("🌍 Image Text Translator")
    st.write("Upload an image containing text, and I'll help you translate it!")

    try:
        # Initialize services
        vision_service, translator_service, speech_service = init_services()

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg', 'bmp'],
            help="Upload an image containing text you want to translate"
        )

        # Target language selection
        target_language = st.selectbox(
            "Select target language",
            list(LANGUAGES.keys()),
            index=1,  # Default to Spanish
            help="Choose the language you want to translate to"
        )

        if uploaded_file is not None:
            # Display the uploaded image
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Uploaded Image")
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)

            # Process button
            if st.button("Extract and Translate", type="primary"):
                with st.spinner("Processing image..."):
                    # Extract text
                    image_bytes = io.BytesIO(uploaded_file.getvalue())
                    extracted_text = vision_service.extract_text(image_bytes)

                    if not extracted_text:
                        st.error("No text could be extracted from the image. Please try another image.")
                        return

                    # Display extracted text
                    with col2:
                        st.subheader("Extracted Text")
                        st.write(extracted_text)
                        
                        # Generate original audio
                        with st.spinner("Generating original audio..."):
                            original_audio = speech_service.text_to_speech(
                                extracted_text,
                                LANGUAGES['English']['speech_code']
                            )
                            
                        # Display audio controls if generation was successful
                        if original_audio:
                            st.audio(original_audio, format="audio/wav")
                            st.download_button(
                                "💾 Download Original Audio",
                                data=original_audio,
                                file_name="original_audio.wav",
                                mime="audio/wav"
                            )
                        else:
                            st.error("Failed to generate original audio")

                    # Translate text
                    with st.spinner(f"Translating to {target_language}..."):
                        translated_text = translator_service.translate_text(
                            extracted_text,
                            LANGUAGES[target_language]['code']
                        )

                    if translated_text:
                        # Translated text audio controls
                        st.subheader(f"Translation ({target_language})")
                        st.write(translated_text)

                        # Generate translated audio first
                        with st.spinner("Generating translated audio..."):
                            translated_audio = speech_service.text_to_speech(
                                translated_text,
                                LANGUAGES[target_language]['speech_code']
                            )
                            
                        # Display audio controls if generation was successful
                        if translated_audio:
                            st.audio(translated_audio, format="audio/wav")
                            st.download_button(
                                "💾 Download Translated Audio",
                                data=translated_audio,
                                file_name=f"translated_audio_{LANGUAGES[target_language]['code']}.wav",
                                mime="audio/wav"
                            )
                        else:
                            st.error("Failed to generate translated audio")


                        # Add download buttons for text
                        col3, col4 = st.columns(2)
                        with col3:
                            st.download_button(
                                "📥 Download Original Text",
                                extracted_text,
                                file_name="original_text.txt",
                                mime="text/plain",
                                key="download_original_text"
                            )
                        with col4:
                            st.download_button(
                                "📥 Download Translation",
                                translated_text,
                                file_name=f"translated_text_{LANGUAGES[target_language]['code']}.txt",
                                mime="text/plain",
                                key="download_translated_text"
                            )
                    else:
                        st.error("Translation failed. Please try again.")

        # Add usage instructions in sidebar
        with st.sidebar:
            st.header("📝 Instructions")
            st.markdown("""
            1. Upload an image containing text
            2. Select your target translation language
            3. Click 'Extract and Translate'
            4. Listen to and download the audio files
            5. Download the text files if needed
            
            **Supported Languages:**
            """)
            for lang in LANGUAGES.keys():
                st.markdown(f"- {lang}")

            st.header("ℹ️ About")
            st.markdown("""
            This app uses Azure AI services to:
            - Extract text from images (OCR)
            - Translate text between languages
            - Convert text to speech
            
            For best results:
            - Use clear, well-lit images
            - Ensure text is readable
            - Avoid handwritten text
            """)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")

if __name__ == "__main__":
    main()
