import logging

from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

from .exceptions import OutOfRetriesException

log: logging.Logger = logging.getLogger(__name__)


class Image:
    def __init__(self, service_file: str, image_uri: str) -> None:
        self.google = vision.ImageAnnotatorClient(
            credentials=service_account.Credentials.from_service_account_file(service_file)
        )

        self.image = types.Image()
        self.image.source.image_uri = image_uri

    def get_text(self) -> None:
        log.info("Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD.")
        attempts = 0
        while attempts < 5:
            attempts += 1
            response = self.google.text_detection(image=self.image)
            try:
                response.text_annotations[0]
            except IndexError:
                pass
            else:
                self.text_found = response.text_annotations
                break

        if attempts == 5:
            raise OutOfRetriesException()
