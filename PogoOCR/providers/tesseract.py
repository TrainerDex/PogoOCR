import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Union
from uuid import UUID, uuid4

import iso639
import pytesseract
import pytz
from babel import Locale
from PIL import Image

from PogoOCR.constants import Locales
from PogoOCR.exceptions import OCRAttemptsExhausted
from PogoOCR.images import Screenshot
from PogoOCR.providers.interface import IProvider, IRequest, IResponse

logger: logging.Logger = logging.getLogger(__name__)


class TesseractRequest(IRequest):
    # Track number of attempts to avoid infinite loop
    ATTEMPT_LIMIT: int = 5
    _attempts_made: int = 0
    _last_attempt_dt: Union[datetime, None] = None

    def __init__(
        self,
        screenshot: Screenshot,
        locale: Locale = Locales.ENGLISH,
    ) -> None:
        self.uuid: UUID = uuid4()
        self.locale = locale
        self.initalized_at: datetime = datetime.now(pytz.UTC)
        self._screenshot: Screenshot = screenshot

    @property
    def attempts_made(self) -> int:
        return self._attempts_made

    @property
    def last_attempt_dt(self) -> Union[datetime, None]:
        return self._last_attempt_dt

    @property
    def attempts_remaining(self) -> int:
        return self.ATTEMPT_LIMIT - self.attempts_made

    @property
    def attempts_allowed(self) -> int:
        return self.ATTEMPT_LIMIT

    def increment_attempts(self) -> None:
        self._attempts_made += 1
        self._last_attempt_dt = datetime.now(pytz.UTC)

    def __str__(self) -> str:
        return f"<TesseractRequest uuid: {self.uuid} initalized_at: {self.initalized_at.isoformat()} screenshot: {self.screenshot}>"


@dataclass
class TesseractReponse(IResponse):
    request: TesseractRequest
    annotation: str

    @property
    def attempts_made(self) -> int:
        return self.request.attempts_made

    @property
    def attempted_allowed(self) -> int:
        return self.request.attempts_allowed

    @property
    def content(self) -> str:
        return self.annotation


class TesseractClient(IProvider):
    def _resolve_language(self, locale: Locale) -> str:
        return iso639.to_iso639_2(locale.language)

    def _modify_image(self, screenshot: Screenshot) -> Image:
        image = screenshot.image
        return image.resize((image.width * 3, image.height * 3))

    def detect_text(self, request: "TesseractRequest") -> TesseractReponse:
        logger.info(
            "Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD."
        )
        while request.attempts_remaining > 0:
            request.increment_attempts()
            logger.debug(
                f"Starting attempt #{request.attempts_made} of {request.attempts_allowed} for {request}"
            )
            annotation: str = pytesseract.image_to_string(
                self._modify_image(request.screenshot), self._resolve_language(request.locale)
            )
            if not annotation:
                logger.debug(
                    f"Attempt #{request.attempts_made} of {request.attempts_allowed} for {request} failed."
                )
                continue
            else:
                logger.debug(
                    f"Attempt #{request.attempts_made} of {request.attempts_allowed} for {request} succeeded."
                )
                return TesseractReponse(request=request, annotation=annotation)
        else:
            raise OCRAttemptsExhausted(f"Request {request} exhausted all attempts.")

    def open_request(
        self,
        screenshot: Screenshot,
        locale: Locale = Locales.ENGLISH,
    ) -> "TesseractRequest":
        request = TesseractRequest(screenshot=screenshot, locale=locale)
        logger.debug(f"Created Cloud Vision Request: {request}")
        return request
