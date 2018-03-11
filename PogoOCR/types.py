from .cloudvision import Image
import re


class Trainer():
    
    def __init__(self, image):
        self.cvimage = Image(image)
        self.image = self.cvimage.image
        
    def get_text(self):
        self.text = self.cvimage.text_detection()
    
    @property
    def username(self):
        return re.search('([A-Za-z0-9]+)\\n\& ([^\\n]+)', self.text[0].description).group(1)
        
    @property
    def buddy_name(self):
        return re.search('([A-Za-z0-9]+)\\n\& ([^\\n]+)', self.text[0].description).group(2)
