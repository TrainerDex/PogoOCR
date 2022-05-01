from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from babel import Locale

from PogoOCR.constants import Locales

if TYPE_CHECKING:
    from PogoOCR.images import Screenshot


class IRequest:
    uuid: UUID = uuid4()
    locale: Locale = Locales.ENGLISH
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
        locale: Locale = Locales.ENGLISH,
    ) -> "IRequest":
        raise NotImplementedError
