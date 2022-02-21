from enum import Enum

from PogoOCR.providers.cloudvision import CloudVisionClient


class Providers(Enum):
    GOOGLE = CloudVisionClient
