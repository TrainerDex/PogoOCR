from decimal import Decimal
from typing import Optional
from colour import Color
from dataclasses import dataclass


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
    faction: Faction
    faction_confidence: float
    username: Optional[str] = None
    buddy: Optional[str] = None
    level: Optional[int] = None
    travel_km: Optional[Decimal] = None
    capture_total: Optional[int] = None
    pokestops_visited: Optional[int] = None
    total_xp: Optional[int] = None
