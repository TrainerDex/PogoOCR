from io import BytesIO
import logging
import pytz
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Union
from uuid import UUID, uuid4

from google.auth.exceptions import GoogleAuthError
from google.cloud import vision
from google.oauth2 import service_account
from PogoOCR.constants import Language

from PogoOCR.images import Screenshot

from PogoOCR.exceptions import (
    CloudVisionAuthenticationException,
    CloudVisionTextAnnotationException,
    OCRAttemptsExhausted,
)
from PogoOCR.providers.interface import IProvider, IResponse, IRequest


logger: logging.Logger = logging.getLogger(__name__)


class CloudVisionRequest(IRequest):
    # Track number of attempts to avoid infinite loop
    ATTEMPT_LIMIT: int = 5
    _attempts_made: int = 0
    _last_attempt_dt: Union[datetime, None] = None

    def __init__(
        self,
        client: "CloudVisionClient",
        screenshot: Screenshot,
        language: Language = Language.ENGLISH,
    ) -> None:
        self.uuid: UUID = uuid4()
        self.language = language
        self.initalized_at: datetime = datetime.now(pytz.UTC)
        self._client: "CloudVisionClient" = client
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
        return f"<CloudVisionRequest uuid: {self.uuid} initalized_at: {self.initalized_at.isoformat()} screenshot: {self.screenshot}>"


@dataclass
class CloudVisionReponse(IResponse):
    request: CloudVisionRequest
    entity: vision.EntityAnnotation

    @property
    def attempts_made(self) -> int:
        return self.request.attempts_made

    @property
    def attempted_allowed(self) -> int:
        return self.request.attempts_allowed

    @property
    def content(self) -> str:
        return self.entity.description

    @property
    def locale(self) -> str:
        return self.entity.locale


class CloudVisionClient(IProvider):
    def __init__(self, credentials: service_account.Credentials):
        try:
            self.client = vision.ImageAnnotatorClient(credentials=credentials)
        except GoogleAuthError as e:
            raise CloudVisionAuthenticationException() from e

    @staticmethod
    def _to_google_image(screenshot: Screenshot) -> vision.Image:
        bytes_io = BytesIO()
        screenshot.image.save(bytes_io, format="PNG")
        bytes_io.seek(0)
        return vision.Image(content=bytes_io.read())

    def _detect_text(self, screenshot: Screenshot) -> vision.EntityAnnotation:
        gimage: vision.Image = self._to_google_image(screenshot)
        response: vision.AnnotateImageResponse = self.client.text_detection(image=gimage)
        text_annotations: Sequence[vision.EntityAnnotation] = response.text_annotations
        try:
            return text_annotations[0]
        except IndexError:
            raise CloudVisionTextAnnotationException()

    def detect_text(self, request: "CloudVisionRequest") -> CloudVisionReponse:
        logger.info(
            "Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD."
        )
        while request.attempts_remaining > 0:
            request.increment_attempts()
            logger.debug(
                f"Starting attempt #{request.attempts_made} of {request.attempts_allowed} for {request}"
            )
            try:
                annotation: vision.EntityAnnotation = self._detect_text(request.screenshot)
            except CloudVisionTextAnnotationException:
                logger.debug(
                    f"Attempt #{request.attempts_made} of {request.attempts_allowed} for {request} failed."
                )
                continue
            else:
                logger.debug(
                    f"Attempt #{request.attempts_made} of {request.attempts_allowed} for {request} succeeded."
                )
                return CloudVisionReponse(request=request, entity=annotation)
        else:
            raise OCRAttemptsExhausted(f"Request {request} exhausted all attempts.")

    def open_request(
        self,
        screenshot: Screenshot,
        language: Language = Language.ENGLISH,
    ) -> "CloudVisionRequest":
        request = CloudVisionRequest(client=self.client, screenshot=screenshot)
        logger.debug(f"Created Cloud Vision Request: {request}")
        return request
