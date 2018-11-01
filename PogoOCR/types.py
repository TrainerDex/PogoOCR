from .cloudvision import Image
import re

class TrainerTop(Image):
    
    @property
    def username(self):
        return re.search('([A-Za-z0-9]+)\\n(?:\&|et|con|e) ?([^\\n]+)', self.text_found[0].description).group(1)
        
    @property
    def buddy_name(self):
        return re.search('([A-Za-z0-9]+)\\n(?:\&|et|con|e) ?([^\\n]+)', self.text_found[0].description).group(2)
