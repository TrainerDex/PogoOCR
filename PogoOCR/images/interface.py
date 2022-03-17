import hashlib
import requests
from io import BytesIO
from PIL import Image
from typing import TYPE_CHECKING, Any, Coroutine, Literal, Optional, Union, overload


try:
    import aiohttp
except ImportError:
    aiohttp = None

if TYPE_CHECKING:
    from PogoOCR.images import ScreenshotClass
    from PogoOCR.providers.interface import IResponse
    from typing_extensions import Self

URL = str


class Screenshot:
    _url: Optional[URL] = None
    _content: bytes = None
    _md5: "hashlib._Hash" = None
    _klass: "ScreenshotClass" = None

    @overload
    def __init__(self, *, url: URL):
        ...

    @overload
    def __init__(self, *, content: bytes):
        ...

    def __init__(
        self,
        *,
        url: Optional[URL] = None,
        content: Optional[bytes] = None,
        klass: "ScreenshotClass" = None,
    ) -> None:
        self._url = url
        self._content = content
        self._klass = klass

    @property
    def url(self) -> Optional[URL]:
        return self._url

    @property
    def has_content(self) -> bool:
        return self._content is not None

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def image(self) -> Union[Image.Image, None]:
        """A Pillow Image object, if the content is an image

        Returns:
            Image.Image: If the content is an image, otherwise None
        """
        if self.has_content:
            return Image.open(BytesIO(self.content))
        return None

    @property
    def klass(self) -> "ScreenshotClass":
        return self._klass

    def _get_content(self) -> None:
        self._content = requests.get(self._url).content

    async def _async_get_content(self) -> None:
        if aiohttp is None:
            raise RuntimeError("aiohttp is not installed")
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as resp:
                self._content = await resp.read()

    @overload
    def get_content(self) -> None:
        ...

    @overload
    def get_content(self, *, asyncronous: Literal[False]) -> None:
        ...

    @overload
    async def get_content(self, *, asyncronous: Literal[True]) -> None:
        ...

    def get_content(self, *, asyncronous: bool = False) -> Union[None, Coroutine[Any, Any, None]]:
        if not self._url:
            raise ValueError("No URL provided")

        if asyncronous:
            return self._async_get_content()
        else:
            return self._get_content()

    @classmethod
    def _from_url(cls, url: URL, klass: "ScreenshotClass") -> "Self":
        obj = cls(url=url, klass=klass)
        obj.get_content(asyncronous=False)
        return obj

    @classmethod
    async def _async_from_url(cls, url: URL, klass: "ScreenshotClass") -> "Self":
        obj = cls(url=url, klass=klass)
        await obj.get_content(asyncronous=True)
        return obj

    @overload
    @classmethod
    def from_url(cls, url: URL, klass: "ScreenshotClass") -> "Self":
        ...

    @overload
    @classmethod
    def from_url(
        cls, url: URL, klass: "ScreenshotClass", *, asyncronous: Literal[False]
    ) -> "Self":
        ...

    @overload
    @classmethod
    async def from_url(
        cls, url: URL, klass: "ScreenshotClass", *, asyncronous: Literal[True]
    ) -> "Self":
        ...

    @classmethod
    def from_url(
        cls, url: URL, klass: "ScreenshotClass", *, asyncronous: bool = False
    ) -> Union["Self", Coroutine[Any, Any, "Self"]]:
        if asyncronous:
            return cls._async_from_url(url, klass)
        else:
            return cls._from_url(url, klass)

    @classmethod
    def from_bytes(cls, content: bytes) -> "Self":
        return cls(content=content)

    def _calculate_md5(self) -> None:
        if self.content:
            self._md5 = hashlib.md5(self.content)

    @property
    def md5(self) -> Union[str, None]:
        if self._md5 is None:
            self._calculate_md5()
        if self._md5:
            return self._md5.hexdigest()

    def __str__(self) -> str:
        if self.content and not self.url:
            return f"<Screenshot {self.md5}>"
        elif self.content and self.url:
            return f"<Screenshot {self.md5} from {self.url}>"
        elif not self.content and self.url:
            return f"<Screenshot from {self.url} (not downloaded)>"
        else:
            return f"<Screenshot {self.md5}>"


class IView:
    def __init__(self, response: "IResponse") -> None:
        self._response = response
        self.language = self._response.request.language
