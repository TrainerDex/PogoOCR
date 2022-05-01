from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

import Levenshtein
from colour import Color

if TYPE_CHECKING:
    from PogoOCR.providers.interface import IResponse


@dataclass
class Faction:
    id: int
    slug: str
    color: Color

    @property
    def colour(self) -> Color:
        return self.color

    @property
    def name(self):
        return self.slug.capitalize()


@dataclass
class ActivityViewData:
    _response: "IResponse" = field(default=None, compare=False)
    faction: Optional[Faction] = None
    faction_confidence: Optional[float] = field(default=None, compare=False)
    username: Optional[str] = None
    buddy: Optional[str] = None
    level: Optional[int] = None
    travel_km: Optional[Decimal] = None
    capture_total: Optional[int] = None
    pokestops_visited: Optional[int] = None
    total_xp: Optional[int] = None

    def compare_username(self, username: str) -> bool:
        if self.username is None:
            return False
        return Levenshtein.ratio(self.username.casefold(), username.casefold()) > 0.8
