from enum import Enum

from PogoOCR.providers.cloudvision import CloudVisionClient  # noqa: F401


class Providers(Enum):
    GOOGLE = CloudVisionClient
