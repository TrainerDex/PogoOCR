from .cloudvision import Image
import re
from itertools import islice

class ProfileSelf(Image):
    
    @property
    def username(self):
        return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(1)
        
    @property
    def buddy_name(self):
        return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(2)
    
    def find_stats(self):
        try:
            left_split = self.text_found[0].description.split('TOTAL ACTIVITY')
        except AttributeError:
            print('Please run .get_text() first!')
            return
        
        if len(left_split) == 2:
            stats_str_iter = iter([x for x in left_split[1].split('WEEKLY PROGRESS')[0].split('\n') if x])
            del left_split
            combo_stats = list(iter(lambda: tuple(islice(stats_str_iter,2)), ()))
            del stats_str_iter
            num_stats_found = 0
            for x in combo_stats:
                if x[0] == 'Distance Walked':
                    self.km_walked = float(x[1].strip().replace(',', '').replace('.', '').split(' ')[0])
                elif x[0] == 'Pokémon Caught':
                    self.catches = int(x[1].strip().replace(',', '').replace('.', '').replace(' ', ''))
                elif x[0] == 'PokéStops Visited:':
                    self.pokestops = int(x[1].strip().replace(',', '').replace('.', '').replace(' ', ''))
                elif x[0] == 'Total XP:' or x[0] == 'XP Total XP:':
                    self.total_xp = int(x[1].strip().replace(',', '').replace('.', '').replace(' ', ''))
                elif x[0] == 'Start Date:':
                    self.start_date_text = x[1].strip()
                else:
                    pass
                num_stats_found += 1
            print(f"Found {num_stats_found} stat(s)")
            print(combo_stats)
            del combo_stats
            
        else:
            del left_split

class Badge(Image):
    
    @property
    def badge(self):
        raise NotImplementedError
            
    @property
    def value(self):
        raise NotImplementedError
    
class Pokédex(Image):
    
    @property
    def gen1(self):
        raise NotImplementedError
            
    @property
    def gen2(self):
        raise NotImplementedError
            
    @property
    def gen3(self):
        raise NotImplementedError
            
    @property
    def gen4(self):
        raise NotImplementedError
