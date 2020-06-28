from .cloudvision import Image
import re
from decimal import Decimal
from datetime import datetime

class ProfileSelf(Image):
	
	def __init__(self, service_file, image_content=None, image_uri=None):
		super().__init__(service_file, image_content=image_content, image_uri=image_uri)
		self.locale = 'en'
		self.number_locale = ',.'
		# This is messy, I might put the lookups in their own .json files and load those.
		# TODO: Look into if I can package .json files with pypi projects.
		self.pattern_lookups = {
			'fr': {
				'travel_km' : r'Distance\smarchée\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Pok[ée]mon\sattrap[ée]s\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'Pok[ée]Stops visit[ée]s\n((?:[,.\s]?\d{1,3})+)',
				'total_xp' : r'Total\sde\sPX\s?[;:：]?\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Date\sde\sd[ée]but\n(\d{2}\/\d{2}\/\d{4})',
				'start_date_format' : '%d/%m/%Y',
				},
			'de': {
				'travel_km' : r'Gelaufene\sDistanz\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Gefangene Pok[ée]mon\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:Besuchte\sPok[ée]Stops[;:：]?|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'Gesamt-EP\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Startdatum\n(\d{2}.\d{2}.\d{4})',
				'start_date_format' : '%d.%m.%Y',
				},
			'it': {
				'travel_km' : r'Distanza\spercorsa\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Pok[ée]mon catturati\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:Pok[ée]stop\svisitati[;:：]?|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'Totale\sPE\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Data\sdi\sinizio\n(\d{2}\/\d{2}\/\d{4})',
				'start_date_format' : '%d/%m/%Y',
				},
			'ja': {
				'travel_km' : r'歩いた距離\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'つかまえたポケモン\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'訪れたポケストップ\n((?:[,.\s]?\d{1,3})+)',
				'total_xp' : r'(?:トータルXP|TOTAL XP)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'start_date' : r'始めた日\n(\d{4}\/\d{2}\/\d{2})',
				'start_date_format' : '%Y/%m/%d',
				},
			'ko': {
				'travel_km' : r'걸은\s거리\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'잡은\s포켓몬\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:방문한\s포켓스톱|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'Total XP\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'시작한\s날\n(\d{4}\/\d{2}\/\d{2})',
				'start_date_format' : '%Y/%m/%d',
				},
			'es': {
				'travel_km' : r'Distancia\scaminando\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Pok[ée]mon atrapados\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:Pok[ée]paradas\svisitadas[;:：]?|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'Total\sde\sPX\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Fecha\sde\sinicio\n(\d{2}\/\d{2}\/\d{4})',
				'start_date_format' : '%d/%m/%Y',
				},
			'zh_hant': {
				'travel_km' : r'步行距離\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'捉到的寶可夢\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:拜訪過的寶可補給站\s?[;:：]?|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'總XP\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'開始日\n(\d{4}\/\d{1,2}\/\d{1,2})',
				'start_date_format' : '%Y/%m/%d',
				},
			'en': {
				'travel_km' : r'Distance Walked\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Pok[ée]mon\sCaught\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'Pok[ée]Stops\sVisited[;:：]?\n((?:[,.\s]?\d{1,3})+)',
				'total_xp' : r'Total\sXP[;:：]?\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Start\sDate[;:：]?\n(\d{1,2}\/\d{1,2}\/\d{4})',
				'start_date_format' : '%m/%d/%Y',
				},
			'pt_br': {
				'travel_km' : r'Dist[âa]ncia\sa\sp[ée]\n((?:\d{1,3}[,.\s])?\d{1,3}[,.]\d{1,2})\skm',
				'capture_total' : r'Pok[ée]mon pegos\n((?:[,.\s]?\d{1,3})+)',
				'pokestops_visited' : r'(?:Pok[ée]paradas\svisitadas[;:：]?|Pok[ée]Stops\sVisited[;:：]?)\n((?:[,.\s]?\d{1,3})+)', # Found a mismatch between the ZeChrales translation files, could indicate a recent string change
				'total_xp' : r'Total\sde\sPE[;:：]?\n((?:[,.\s]?\d{1,3})+)',
				'start_date' : r'Data\sde\sin[íi]cio\n(\d{1,2}\/\d{1,2}\/\d{4})',
				'start_date_format' : '%d/%m/%Y',
				},
		}
	
	def get_text(self, force=False):
		# Check if an API call needs to be made. If not, don't make a call. Prevents accidental extra calls to a premium API
		if force or not hasattr(self,'text_found'):
			super().get_text()
		
		# Try to work out language:
		locale_lookup = [
			('fr', r'(?:(?:Activit[ée]s\stotales)|(?:PROGR[ÈE]S\sDE\sLA\sSEMAINE))'),
			('de', r'(?:(?:Aktivit[äa]tsstatistik)|(?:W[ÖO]CHENTLICHER\sFORTSCHRITT))'),
			('it', r'(?:(?:Riepilogo\sattivit[àa])|(?:PROGRESSI\sSETTIMANALI))'),
			('ja', r'(?:(?:アクティビティ)|(?:ウィークリー))'),
			('ko', r'(?:(?:활동)|(?:주간\s피트니스))'),
			('es', r'(?:(?:Total\sde\sactividades)|(?:PROGRESO\sSEMANAL))'),
			('zh_hant', r'(?:(?:活動紀錄)|(?:本週成果))'),
			('en', r'(?:(?:Total\sActivity)|(?:WEEKLY\sPROGRESS))'),
			('pt_br', r'(?:(?:Total\sde\satividades)|(?:PROGRESSO\sSEMANAL))'),
		]
		for locale, pattern in locale_lookup:
			if re.search(pattern, self.text_found[0].description, re.IGNORECASE):
				self.locale = locale
				break
		
		# Try to work out number format
		number_locale_lookup = [
			(',.', r'\d,(?:\d{3})(\.\d)?'),
			('.,', r'\d\.(?:\d{3})(,\d)?'),
			(' ,', r'\d\s(?:\d{3})(,\d)?'),
		]
		for number_locale, pattern in number_locale_lookup:
			if re.search(pattern, self.text_found[0].description):
				self.number_locale = number_locale
				break
	
	@property
	def username(self):
		try:
			return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(1)
		except:
			return None
		
	@property
	def buddy_name(self):
		try:
			return re.search(r'([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)', self.text_found[0].description).group(2)
		except:
			return None
	
	@property
	def travel_km(self):
		try:
			result = re.search(self.pattern_lookups[self.locale]['travel_km'], self.text_found[0].description, re.IGNORECASE).group(1).replace(self.number_locale[0], '').replace(self.number_locale[1], '.').strip()
			return Decimal(result)
		except:
			return None
	
	@property
	def capture_total(self):
		try:
			result = re.search(self.pattern_lookups[self.locale]['capture_total'], self.text_found[0].description, re.IGNORECASE).group(1).replace(self.number_locale[0], '').replace(self.number_locale[1], '.').strip()
			return int(result)
		except:
			return None
	
	@property
	def pokestops_visited(self):
		try:
			result = re.search(self.pattern_lookups[self.locale]['pokestops_visited'], self.text_found[0].description, re.IGNORECASE).group(1).replace(self.number_locale[0], '').replace(self.number_locale[1], '.').strip()
			return int(result)
		except:
			return None
	
	@property
	def total_xp(self):
		try:
			result = re.search(self.pattern_lookups[self.locale]['total_xp'], self.text_found[0].description, re.IGNORECASE).group(1).replace(self.number_locale[0], '').replace(self.number_locale[1], '.').strip()
			return int(result)
		except:
			return None
	
	@property
	def start_date(self):
		try:
			result = re.search(self.pattern_lookups[self.locale]['start_date'], self.text_found[0].description, re.IGNORECASE).group(1)
			return datetime.strptime(result, self.pattern_lookups[self.locale]['start_date_format']).date()
		except:
			return None
	
	def find_stats(self):
		return self.get_text(force=False)
	
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
