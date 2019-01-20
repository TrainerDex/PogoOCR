import io
from django.conf import settings
from google.cloud import vision
from google.cloud.vision import types
from google.auth.credentials import Credentials
from PIL import Image

class Image:
    """
    Only to be ran from inside the Django environment
    """
    
    def __init__(self, image_uri):
        self.google = vision.ImageAnnotatorClient(credentials=Credentials(token=settings.GOOGLE_API_TOKEN))
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
        
