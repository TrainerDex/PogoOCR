import datetime
import decimal
import json
import logging
import os
import re
from string import digits
from typing import Optional

from babel.numbers import NumberFormatError
from dateutil.parser import parse as parse_date

from .cloudvision import Image
from .numbers import parse_decimal, parse_number

log: logging.Logger = logging.getLogger(__name__)


class ProfileSelf(Image):
    def __init__(self, service_file, image_content=None, image_uri=None) -> None:
        super().__init__(service_file, image_content=image_content, image_uri=image_uri)
        self.locale = "en"
        self.numeric_locale = {}
        with open(os.path.join(os.path.dirname(__file__), "pattern_lookups.json"), "r") as f:
            self.pattern_lookups = json.load(f)

    def get_text(self, force: Optional[bool] = False) -> None:
        # Check if an API call needs to be made.
        # Prevents accidental extra calls to a premium API
        if force or not hasattr(self, "text_found"):
            super().get_text()

        # Try to work out locale:
        locale_lookup = [
            ("fr", r"(?:(?:Activit[ée]s\stotales)|(?:PROGR[ÈE]S\sDE\sLA\sSEMAINE))"),
            ("de", r"(?:(?:Aktivit[äa]tsstatistik)|(?:W[ÖO]CHENTLICHER\sFORTSCHRITT))"),
            ("it", r"(?:(?:Riepilogo\sattivit[àa])|(?:PROGRESSI\sSETTIMANALI))"),
            ("ja", r"(?:(?:アクティビティ)|(?:ウィークリー))"),
            ("ko", r"(?:(?:활동)|(?:주간\s피트니스))"),
            ("es", r"(?:(?:Total\sde\sactividades)|(?:PROGRESO\sSEMANAL))"),
            ("zh", r"(?:(?:活動紀錄)|(?:本週成果))"),
            ("en", r"(?:(?:Total\sActivity)|(?:WEEKLY\sPROGRESS))"),
            ("pt", r"(?:(?:Total\sde\satividades)|(?:PROGRESSO\sSEMANAL))"),
            ("th", r"(?:(?:กิจกรรมทั้งหมด)|(?:ความคืบหน้าประจำสัปดาห์))"),
        ]
        for locale, pattern in locale_lookup:
            if re.search(pattern, self.text_found[0].description, re.IGNORECASE):
                self.locale = locale
                break

        # Since the only stat that is a decimal is travel_km, we will check that.
        try:
            travel_km = (
                re.search(
                    self.pattern_lookups[self.locale]["travel_km"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace("km", "")
                .strip()
                .replace(" ", "\xa0")
            )
        except (decimal.InvalidOperation, TypeError):
            pass
        else:
            translated = travel_km.translate(str.maketrans("", "", digits))
            self.numeric_locale["decimal"] = translated[-1]
            if len(translated) > 1:
                self.numeric_locale["group"] = translated[-2]

        # If travel_km wasn't big enough to get the group for numeric_locale, try total_xp
        try:
            total_xp = (
                re.search(
                    self.pattern_lookups[self.locale]["total_xp"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .strip()
                .replace(" ", "\xa0")
            )
        except (ValueError, TypeError):
            # Assume English
            self.numeric_locale["group"] = ","
        else:
            translated = total_xp.translate(str.maketrans("", "", digits))
            self.numeric_locale["group"] = translated[0]

    @property
    def username(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[1]
        except TypeError as e:
            log.exception("username failed to return")
            return None

    @property
    def buddy_name(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[2]
        except TypeError as e:
            log.exception("buddy_name failed to return")
            return None

    @property
    def travel_km(self) -> Optional[decimal.Decimal]:
        try:
            result = (
                re.search(
                    self.pattern_lookups[self.locale]["travel_km"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace("km", "")
                .strip()
            )
            return parse_decimal(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError) as e:
            log.exception("travel_km failed to return")
            return None

    @property
    def capture_total(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale]["capture_total"],
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError) as e:
            log.exception("capture_total failed to return")
            return None

    @property
    def pokestops_visited(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale]["pokestops_visited"],
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError) as e:
            log.exception("pokestops_visited failed to return")
            return None

    @property
    def total_xp(self) -> Optional[int]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale]["total_xp"],
                self.text_found[0].description,
                re.IGNORECASE,
            )[1].strip()
            return parse_number(result, locale=self.numeric_locale)
        except (NumberFormatError, TypeError) as e:
            log.exception("total_xp failed to return")
            return None

    @property
    def start_date(self) -> Optional[datetime.date]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale]["start_date"],
                self.text_found[0].description,
                re.IGNORECASE,
            )[1]
            return parse_date(result).date()
        except (ValueError, OverflowError, TypeError) as e:
            log.exception("start_date failed to return")
            return None

    def find_stats(self):
        return self.get_text(force=False)
