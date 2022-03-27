import math
import re
from colour import Color
from decimal import Decimal
from typing import Tuple, Union

from PogoOCR.constants import __ALL_FACTIONS__
from PogoOCR.dataclasses import ActivityViewData, Faction
from PogoOCR.images.interface import IView
from PogoOCR.utils import calculate_colour_distance, rgb2color


class ActivityView(IView):
    def _identify_faction(self) -> Tuple[Faction, float]:
        """Identify the faction of the player using the colour on the border of the Acitivity View

        Returns:
            Tuple[Faction, float]: A 2-tuple of the best guess of the faction and the confidence of the guess
        """
        image = self._response.request.screenshot.image.convert("RGB")

        left_pixel_location: Tuple[int, int] = (2, math.ceil(image.height / 2))
        left_pixel_color: Color = rgb2color(*image.getpixel(left_pixel_location))
        left_best_guess: Faction = sorted(
            __ALL_FACTIONS__,
            key=lambda faction: calculate_colour_distance(faction.color, left_pixel_color),
        )[0]
        left_distance: float = calculate_colour_distance(left_pixel_color, left_best_guess.color)

        right_pixel_location: Tuple[int, int] = (image.width - 2, math.ceil(image.height / 2))
        right_pixel_color: Color = rgb2color(*image.getpixel(right_pixel_location))
        right_best_guess: Faction = sorted(
            __ALL_FACTIONS__,
            key=lambda faction: calculate_colour_distance(faction.color, right_pixel_color),
        )[0]
        right_distance: float = calculate_colour_distance(
            right_pixel_color, right_best_guess.color
        )

        distance, best_guess = sorted(
            [(left_distance, left_best_guess), (right_distance, right_best_guess)],
            key=lambda x: x[0],
        )[0]
        confidence = round(abs(distance - 100) / 100, 3)
        return best_guess, confidence

    def _look_for_username_and_buddy(self) -> Tuple[Union[str, None], Union[str, None]]:
        # TODO: Localization
        match: re.Match = re.search(
            r"(?P<username>[A-Za-z0-9]+)\n\&\s?(?P<buddy>.+)", self._response.content
        )
        if match is None:
            return None, None

        try:
            username = match.group("username")
        except ValueError:
            username = None

        try:
            buddy = match.group("buddy")
        except ValueError:
            buddy = None

        return username, buddy

    def _parse_player_level(self) -> Union[int, None]:
        # match: re.Match = re.search()
        return None

    def _parse_travel_km(self) -> Union[Decimal, None]:
        match: re.Match = re.search(
            r"Distance\s*Walked:?\s*(?P<whole>(?:\d{0,3}[,\.\s]?)+)[,\.\s](?P<decimal>\d{1,2})\s*km",
            self._response.content,
        )
        if match is None:
            return None

        try:
            whole: str = match.group("whole")
            decimal: str = match.group("decimal")
        except ValueError:
            return None

        whole = re.sub("[^0-9]", "", whole)
        return Decimal(f"{whole}.{decimal}")

    def _parse_capture_total(self) -> Union[int, None]:
        match: re.Match = re.search(
            r"Pok[eé]mon\s*Caught:?\s*(?P<total>(?:\d{0,3}[,\.\s]?)+)", self._response.content
        )
        if match is None:
            return None

        try:
            total: str = match.group("total")
        except ValueError:
            return None

        return int(re.sub("[^0-9]", "", total))

    def _parse_pokestops_visited(self) -> Union[int, None]:
        match: re.Match = re.search(
            r"Pok[eé]Stops\s*Visited:?\s*(?P<total>(?:\d{0,3}[,\.\s]?)+)", self._response.content
        )
        if match is None:
            return None

        try:
            total: str = match.group("total")
        except ValueError:
            return None

        return int(re.sub("[^0-9]", "", total))

    def _parse_total_xp(self) -> Union[int, None]:
        match: re.Match = re.search(
            r"Total\s*XP:?\s*(?P<total>(?:\d{0,3}[,\.\s]?)+)", self._response.content
        )
        if match is None:
            return None

        try:
            total: str = match.group("total")
        except ValueError:
            return None

        return int(re.sub("[^0-9]", "", total))

    def _parse_activity_segment(
        self,
    ) -> Tuple[Union[Decimal, None], Union[int, None], Union[int, None], Union[int, None]]:
        travel_km = self._parse_travel_km()
        capture_total = self._parse_capture_total()
        pokestops_visited = self._parse_pokestops_visited()
        total_xp = self._parse_total_xp()
        return travel_km, capture_total, pokestops_visited, total_xp

    def parse(self) -> ActivityViewData:
        faction, faction_confidence = self._identify_faction()
        username, buddy = self._look_for_username_and_buddy()
        level = self._parse_player_level()
        travel_km, capture_total, pokestops_visited, total_xp = self._parse_activity_segment()

        return ActivityViewData(
            _response=self._response,
            faction=faction,
            faction_confidence=faction_confidence,
            username=username,
            buddy=buddy,
            level=level,
            travel_km=travel_km,
            capture_total=capture_total,
            pokestops_visited=pokestops_visited,
            total_xp=total_xp,
        )
