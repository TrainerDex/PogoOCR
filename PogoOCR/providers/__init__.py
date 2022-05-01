from enum import Enum

from PogoOCR.providers.cloudvision import CloudVisionClient
from PogoOCR.providers.tesseract import TesseractClient


class Providers(Enum):
    GOOGLE = CloudVisionClient
    TESSERACT = TesseractClient
