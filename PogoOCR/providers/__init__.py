from enum import Enum

from PogoOCR.providers.tesseract import TesseractClient


try:
    from PogoOCR.providers.cloudvision import CloudVisionClient
except ImportError:
    CloudVisionClient = None


class Providers(Enum):
    GOOGLE = CloudVisionClient
    TESSERACT = TesseractClient
