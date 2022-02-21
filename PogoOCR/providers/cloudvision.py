import logging
from typing import TYPE_CHECKING

from google.cloud.vision import ImageAnnotatorClient
from google.oauth2 import service_account

from ..exceptions import OutOfRetriesException

if TYPE_CHECKING:
    from google.cloud.vision_v1.proto.image_annotator_pb2 import Image
else:
    from google.cloud.vision.types import Image


log: logging.Logger = logging.getLogger(__name__)


class Screenshot:
    def __init__(self, credentials: service_account.Credentials, image_uri: str) -> None:
        self.client = ImageAnnotatorClient(credentials=credentials)

        self.image: Image = Image()
        self.image.source.image_uri = image_uri

    def get_text(self) -> None:
        log.info("Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD.")
        attempts = 0
        while attempts < 5:
            attempts += 1
            response = self.client.text_detection(image=self.image)
            try:
                response.text_annotations[0]
            except IndexError:
                pass
            else:
                self.text_found = response.text_annotations
                break

        if attempts == 5:
            raise OutOfRetriesException()
