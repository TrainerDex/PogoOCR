from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from PogoOCR.constants import Language

if TYPE_CHECKING:
    from PogoOCR.images import Screenshot


class IRequest:
    uuid: UUID = uuid4()
    language: "Language" = Language.ENGLISH
    initalized_at: datetime = None
    _client: "IProvider" = None
    _screenshot: "Screenshot" = None

    @property
    def screenshot(self) -> "Screenshot":
        return self._screenshot


@dataclass
class IResponse:
    request: IRequest

    @property
    def screenshot(self) -> "Screenshot":
        return self.request.screenshot

    @property
    def md5(self) -> str:
        return self.request.screenshot.md5

    @property
    def content(self) -> str:
        raise NotImplementedError

    @property
    def locale(self) -> str:
        raise NotImplementedError


class IProvider:
    @abstractmethod
    def detect_text(self, request: IRequest) -> IResponse:
        raise NotImplementedError

    def open_request(
        self,
        screenshot: "Screenshot",
        language: "Language" = Language.ENGLISH,
    ) -> "IRequest":
        raise NotImplementedError
