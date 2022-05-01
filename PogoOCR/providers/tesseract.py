import logging
import pytz
from dataclasses import dataclass
from datetime import datetime
from typing import Union
from uuid import UUID, uuid4

import pytesseract

from PogoOCR.constants import Language
from PogoOCR.images import Screenshot
from PogoOCR.exceptions import (
    CloudVisionTextAnnotationException,
    OCRAttemptsExhausted,
)
from PogoOCR.providers.interface import IProvider, IResponse, IRequest


logger: logging.Logger = logging.getLogger(__name__)


class TesseractRequest(IRequest):
    # Track number of attempts to avoid infinite loop
    ATTEMPT_LIMIT: int = 5
    _attempts_made: int = 0
    _last_attempt_dt: Union[datetime, None] = None

    def __init__(
        self,
        screenshot: Screenshot,
        language: Language = Language.ENGLISH,
    ) -> None:
        self.uuid: UUID = uuid4()
        self.language = language
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
                request.screenshot.image, request.language.value
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
        language: Language = Language.ENGLISH,
    ) -> "TesseractRequest":
        request = TesseractRequest(screenshot=screenshot)
        logger.debug(f"Created Cloud Vision Request: {request}")
        return request
