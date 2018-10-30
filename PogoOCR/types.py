from .cloudvision import Image
import re


class Trainer():
    
    def __init__(self, image):
        self.cvimage = Image(image)
        self.image = self.cvimage.image
        
    def get_text(self):
        self.cvimage.get_text()
        self.text = self.cvimage.text_found
    
    @property
    def username(self):
        return re.search('([A-Za-z0-9]+)\\n(?:\&|et|con|e) ?([^\\n]+)', self.text[0].description).group(1)
        
    @property
    def buddy_name(self):
        return re.search('([A-Za-z0-9]+)\\n(?:\&|et|con|e) ?([^\\n]+)', self.text[0].description).group(2)
