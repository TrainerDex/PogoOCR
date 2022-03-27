"""
PogoOCR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python tool for running OCR on Pokemon Screenshots using Google Cloud Vision

:copyright: (c) 2020 TrainerDex
:licence: GNU GENERAL PUBLIC LICENSE 3.0

"""

__title__ = "PogoOCR"
__author__ = "JayTurnr"
__licence__ = "GNU GENERAL PUBLIC LICENSE 3.0"
__copyright__ = "2021 TrainerDex"
__version__ = "0.4.0b2"

from .providers.cloudvision import Screenshot  # noqa: F401
from .client import OCRClient  # noqa: F401
from .constants import (  # noqa: F401
    __ALL_FACTIONS__,
    __FACTION_ID_MAPPING__,
    Levels,
    Language,
    TEAMLESS,
    MYSTIC,
    VALOR,
    INSTINCT,
)
from .images import ScreenshotClass  # noqa: F401
