import json
import re
import datetime.date
import decimal.Decimal
from typing import Optional

from dateutil.parser import parse

from .cloudvision import Image


class ProfileSelf(Image):
    def __init__(self, service_file, image_content=None, image_uri=None) -> None:
        super().__init__(service_file, image_content=image_content, image_uri=image_uri)
        self.locale = "en"
        self.number_locale = ",."
        with open("pattern_lookups.json", "r") as f:
            self.pattern_lookups = json.load(f)

    def get_text(self, force: Optional[bool] = False) -> None:
        # Check if an API call needs to be made.
        # Prevents accidental extra calls to a premium API
        if force or not hasattr(self, "text_found"):
            super().get_text()

        # Try to work out language:
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

        # Try to work out number format
        number_locale_lookup = [
            (",.", r"\d,(?:\d{3})(\.\d)?"),
            (".,", r"\d\.(?:\d{3})(,\d)?"),
            (" ,", r"\d\s(?:\d{3})(,\d)?"),
        ]
        for number_locale, pattern in number_locale_lookup:
            if re.search(pattern, self.text_found[0].description):
                self.number_locale = number_locale
                break

    @property
    def username(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[1]
        except TypeError:
            return None

    @property
    def buddy_name(self) -> Optional[str]:
        try:
            return re.search(
                r"([A-Za-z0-9]+)\n(?:\&|et|con|e) ?(.+)", self.text_found[0].description
            )[2]
        except TypeError:
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
                .replace(self.number_locale[0], "")
                .replace(self.number_locale[1], ".")
                .replace("km", "")
                .strip()
            )
            return decimal.Decimal(result)
        except (decimal.InvalidOperation, TypeError):
            return None

    @property
    def capture_total(self) -> Optional[int]:
        try:
            result = (
                re.search(
                    self.pattern_lookups[self.locale]["capture_total"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace(self.number_locale[0], "")
                .replace(self.number_locale[1], ".")
                .strip()
            )
            return int(result)
        except (ValueError, TypeError):
            return None

    @property
    def pokestops_visited(self) -> Optional[int]:
        try:
            result = (
                re.search(
                    self.pattern_lookups[self.locale]["pokestops_visited"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace(self.number_locale[0], "")
                .replace(self.number_locale[1], ".")
                .strip()
            )
            return int(result)
        except (ValueError, TypeError):
            return None

    @property
    def total_xp(self) -> Optional[int]:
        try:
            result = (
                re.search(
                    self.pattern_lookups[self.locale]["total_xp"],
                    self.text_found[0].description,
                    re.IGNORECASE,
                )[1]
                .replace(self.number_locale[0], "")
                .replace(self.number_locale[1], ".")
                .strip()
            )
            return int(result)
        except (ValueError, TypeError):
            return None

    @property
    def start_date(self) -> Optional[datetime.date]:
        try:
            result = re.search(
                self.pattern_lookups[self.locale]["start_date"],
                self.text_found[0].description,
                re.IGNORECASE,
            )[1]
            return parse(result)
        except (ValueError, OverflowError, TypeError):
            return None

    def find_stats(self):
        return self.get_text(force=False)
