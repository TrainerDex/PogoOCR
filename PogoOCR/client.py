from PogoOCR.providers import Providers
from PogoOCR.providers.interface import IProvider


class OCRClient:
    def __init__(self, provider: Providers):
        self.client: IProvider = provider.value()
