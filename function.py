from PIL import Image
from google.cloud import translate
# the pyttsx3 is a library that shows text-to-specch
#synthesizes text in to audio
import pyttsx3
# will print the text that it recognized in the image
import pytesseract

class ImageToText():
    # one time installation
    engine = pyttsx3.init()

    def getText(self,words):
        #Returns the result of a Tesseract OCR run on the image to string
        text = pytesseract.image_to_string(Image.open(words))
        return text

    def speech(text, path):
        text = text.replace('\n', ' ')
        # when spoken, like a pause between sentences.
        engine.say(text)
        # Flush the say() queue and play the audio
        engine.runAndWait()

    def translate(self, text, target):
        # Translates text into the target language
        translate_client = translate.Client()
        # return an order of results for each text
        result = translate_client.translate(text, target_language=target)
        user_input = result['input']
        # the translation of the text
        translated_text = result['translatedText']
        # the language it detected such as "es" refers to spanish
        source_language = result['detectedSourceLanguage']
        return translated_text

