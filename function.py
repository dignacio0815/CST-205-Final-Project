from PIL import Image
from google.cloud import translate
import pyttsx3
import pytesseract

class ImageToText():
    engine = pyttsx3.init()

    def getText(self,words):
        text = pytesseract.image_to_string(Image.open(words))
        return text

    def speech(text, path):
        text = text.replace('\n', ' ')
        engine.say(text)
        engine.runAndWait()

    def translate(self, text, target):
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target)
        user_input = result['input']
        translated_text = result['translatedText']
        source_language = result['detectedSourceLanguage']
        return translated_text
