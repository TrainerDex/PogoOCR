import io
from PIL import Image
from google.cloud import vision
from google.cloud.vision import types

class Image():
    
    def __init__(self, image_uri):
        self.google = vision.ImageAnnotatorClient()
        self.image_uri = image_uri
    
    @property
    def image(self):
        image = types.Image()
        image.source.image_uri = self.image_uri
        return image
    
    def get_text(self):
        print("Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD.")
        response = self.google.text_detection(image=self.image)
        self.text_found = response.text_annotations
        
