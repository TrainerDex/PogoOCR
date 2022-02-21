from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from PogoOCR.image import Screenshot


class IRequest:
    uuid: UUID = uuid4()
    initalized_at: datetime = None
    _client: "IProvider" = None
    _screenshot: "Screenshot" = None

    @property
    def screenshot(self) -> Screenshot:
        return self._screenshot


@dataclass
class IReponse:
    request: IRequest

    @property
    def screenshot(self) -> Screenshot:
        return self.request.screenshot

    @property
    def md5(self) -> str:
        return self.request.screenshot.md5


class IProvider:
    @abstractmethod
    def detect_text(self, request: IRequest) -> IReponse:
        raise NotImplementedError

    def open_request(self, screenshot: Screenshot) -> "IRequest":
        raise NotImplementedError
