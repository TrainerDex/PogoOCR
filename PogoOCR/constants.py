from enum import Enum
from typing import Sequence

from PogoOCR.dataclasses import Faction
from PogoOCR.utils import rgb2color


TEAMLESS = Faction(0, "teamless", rgb2color(0.0, 231.0, 181.0))
MYSTIC = Faction(1, "mystic", rgb2color(6.5, 118.8, 241.6))
VALOR = Faction(2, "valor", rgb2color(255.0, 4.0, 42.0))
INSTINCT = Faction(3, "instinct", rgb2color(253.0, 202.0, 0.1))

__ALL_FACTIONS__ = (TEAMLESS, MYSTIC, VALOR, INSTINCT)
__FACTION_ID_MAPPING__ = {faction.id: faction for faction in __ALL_FACTIONS__}


Levels: Sequence[int] = range(1, 51)


class Language(Enum):
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"
    SPANISH = "es"
    THAI = "th"
    CHINESE_TRADITIONAL = "zh_hant"
    BRAZILIAN_PORTUGUESE = "pt_br"
