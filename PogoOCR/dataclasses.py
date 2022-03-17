from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from colour import Color
from dataclasses import dataclass

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
    _response: "IResponse" = None
    faction: Optional[Faction] = None
    faction_confidence: Optional[float] = None
    username: Optional[str] = None
    buddy: Optional[str] = None
    level: Optional[int] = None
    travel_km: Optional[Decimal] = None
    capture_total: Optional[int] = None
    pokestops_visited: Optional[int] = None
    total_xp: Optional[int] = None
