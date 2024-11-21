# Azure AI Translation App

An interactive web application that extracts text from images, translates it into different languages, and provides text-to-speech functionality using Azure AI services.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
- Copy `.env.example` to `.env`
- Fill in your Azure credentials

5. Run the application:
```bash
streamlit run app.py
```

## Features

- Image text extraction using Azure Computer Vision
- Text translation using Azure Translator
- Text-to-speech using Azure Speech Services
- Support for multiple languages
- Interactive web interface

## Requirements

- Python 3.8+
- Azure subscription with:
  - Computer Vision API
  - Translator API
  - Speech Services
