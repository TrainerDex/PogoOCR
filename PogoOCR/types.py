from .cloudvision import Image
import re

class ProfileTop(Image):
    
    @property
    def username(self):
        return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(1)
        
    @property
    def buddy_name(self):
        return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(2)

class ProfileBottom(Image):
    
    @property
    def start_date_text(self):
        re_pattern = r'(?:(?:Start\s?Date)|(?:始めた日)|(?:Date\s?de\s?début)|(?:Date\s?de\s?debut)|(?:Fecha\s?de\s?inicio)|(?:Startdatum)|(?:Data\s?di\si?nizio)|(?:시작한\s?날)|(?:開始日)|(?:Data\s?de\s?início))(?::|：)?\s?(\d{1,4}\/\d{1,2}\/\d{1,4})'
        return re.search(re_pattern, self.text_found[0].description, re.IGNORECASE).group(1)
    
    @property
    def total_xp(self):
        re_pattern = r'(?:(?:Total\s?XP)|(?:TOTAL\s?XP)|(?:Total\s?de\s?PX)|(?:Gesamt-EP)|(?:Totale\s?PE)|(?:總XP)|(?:Total\s?de\s?PE))\s?(?::|：)?\s?([\d,.]+)'
        return re.search(re_pattern, self.text_found[0].description, re.IGNORECASE).group(1)
        
