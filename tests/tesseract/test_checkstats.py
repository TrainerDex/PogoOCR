import decimal
import logging
import pytest
from typing import TYPE_CHECKING

import PogoOCR
from PogoOCR.constants import VALOR
from PogoOCR.dataclasses import ActivityViewData
from PogoOCR.providers import Providers

if TYPE_CHECKING:
    from PogoOCR.providers.cloudvision import CloudVisionRequest


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

client = PogoOCR.OCRClient(provider=Providers.TESSERACT)


def func(url):
    screenshot = PogoOCR.Screenshot.from_url(
        url=url,
        klass=PogoOCR.ScreenshotClass.ACTIVITY_VIEW,
    )

    request: CloudVisionRequest = client.open_request(screenshot, PogoOCR.Language.ENGLISH)

    view_data: ActivityViewData = client.process_ocr(request)

    # This is not something we're testing
    view_data.faction_confidence = None
    view_data.buddy = None
    view_data.level = None

    return view_data


options = [
    #     (
    #         "fr",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712570150921961512/Screenshot_20200520-083906.jpg",
    #         {
    #             "locale": babel.Locale.parse("fr"),
    #             "numeric_locale": {"group": "\xa0", "decimal": ","},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "de",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712579182416232458/Screenshot_20200520-091452.jpg",
    #         {
    #             "locale": babel.Locale.parse("de"),
    #             "numeric_locale": {"group": ".", "decimal": ","},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "it",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712582940244181073/Screenshot_20200520-092956.jpg",
    #         {
    #             "locale": babel.Locale.parse("it"),
    #             "numeric_locale": {"group": ".", "decimal": ","},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "ja",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712585432520589352/Screenshot_20200520-093943.jpg",
    #         {
    #             "locale": babel.Locale.parse("ja"),
    #             "numeric_locale": {"group": ",", "decimal": "."},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "ko",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712587774309433364/Screenshot_20200520-094915.jpg",
    #         {
    #             "locale": babel.Locale.parse("ko"),
    #             "numeric_locale": {"group": ",", "decimal": "."},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "es",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712590402548662372/Screenshot_20200520-095940.jpg",
    #         {
    #             "locale": babel.Locale.parse("es"),
    #             "numeric_locale": {"group": ".", "decimal": ","},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    #     (
    #         "zh",
    #         "https://cdn.discordapp.com/attachments/339450026076012544/712592915234422784/Screenshot_20200520-100930.jpg",
    #         {
    #             "locale": babel.Locale.parse("zh_hant"),
    #             "numeric_locale": {"group": ",", "decimal": "."},
    #             "username": "JayTurnrTDX",
    #             "travel_km": decimal.Decimal("6170.4"),
    #             "capture_total": 55865,
    #             "pokestops_visited": 42809,
    #             "total_xp": 68315780,
    #         },
    #     ),
    (
        "en",
        "https://cdn.discordapp.com/attachments/543105822629167104/709926063282847834/Screenshot_20200513-013228.jpg",
        ActivityViewData(
            faction=VALOR,
            username="JayTurnrTDX",
            travel_km=decimal.Decimal("6163.7"),
            capture_total=55718,
            pokestops_visited=42807,
            total_xp=68064220,
        ),
    ),
    # (
    # "pt",
    # "https://cdn.discordapp.com/attachments/339450026076012544/712597570421260408/Screenshot_20200520-102802.jpg",
    # {
    # "locale": babel.Locale.parse("pt_br"),
    # "numeric_locale": {"group": ".", "decimal": ","},
    # "username": "JayTurnrTDX",
    # "travel_km": decimal.Decimal("6170.4"),
    # "capture_total": 55865,
    # "pokestops_visited": 42809,
    # "total_xp": 68315780,
    # },
    # ),
    (
        "edge_of_screen",
        "https://cdn.discordapp.com/attachments/329751396222238722/711468207667544095/Screenshot_20200517-074014.png",
        (
            ActivityViewData(
                faction=VALOR,
                username="nerraw1986",
                travel_km=decimal.Decimal("1325.7"),
                capture_total=4721,
                pokestops_visited=3309,  # Real Stat
                total_xp=5421143,
            ),
            ActivityViewData(
                faction=VALOR,
                username="nerraw1986",
                travel_km=decimal.Decimal("1325.7"),
                capture_total=4721,
                pokestops_visited=None,  # Known bug, searching fix, not world ending
                total_xp=5421143,
            ),
        ),
    ),
    # (
    # "fr",
    # "https://cdn.discordapp.com/attachments/370708840850653184/752445686699786270/Screenshot_20200907_103022_com.nianticlabs.pokemongo.jpg",
    # {
    # "locale": babel.Locale.parse("fr"),
    # "numeric_locale": {"group": "\xa0", "decimal": "."},
    # "username": "03icemix",
    # "travel_km": decimal.Decimal("809.1"),
    # "capture_total": 12537,
    # "pokestops_visited": 11633,
    # "total_xp": 11931177,
    # },
    # ),
    (
        "english with non-english numerics",
        "https://cdn.discordapp.com/attachments/370708840850653184/751596341985148958/image0.png",
        ActivityViewData(
            faction=VALOR,
            travel_km=decimal.Decimal("1127.1"),
            capture_total=21543,
            pokestops_visited=10457,
            total_xp=16657146,
        ),
    ),
    (
        "english with but missing travel_km",
        "https://cdn.discordapp.com/attachments/370708840850653184/752889030680510494/Screenshot_20200908-145202.jpg",
        ActivityViewData(
            faction=VALOR,
            capture_total=60062,
            pokestops_visited=44890,
            total_xp=75751423,
        ),
    ),
]


@pytest.mark.parametrize("test_name,input,expected", options)
def test_answer(test_name, input, expected):
    res = func(input)
    logger.debug(res._response.content)
    res._response = None
    if isinstance(expected, tuple):
        assert any([res == e for e in expected])
    else:
        assert res == expected
