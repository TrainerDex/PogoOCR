from PogoOCR.constants import Language
from PogoOCR.images import Screenshot
from PogoOCR.providers import Providers
from PogoOCR.providers.interface import IProvider, IResponse, IRequest


class OCRClient:
    def __init__(self, provider: Providers = Providers.GOOGLE, **kwargs):
        self.client: IProvider = provider.value(**kwargs)

    def open_request(
        self,
        screenshot: Screenshot,
        language: Language = Language.ENGLISH,
    ) -> IRequest:
        return self.client.open_request(screenshot, language)

    def process_ocr(self, request: IRequest):
        if isinstance(request.screenshot.klass.value, str):
            raise NotImplementedError()
        else:
            klass = request.screenshot.klass.value

        response: IResponse = self.client.detect_text(request)
        view = klass(response)
        return view.parse()
