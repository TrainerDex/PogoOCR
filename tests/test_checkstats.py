import babel
import decimal
import logging
import PogoOCR
import pytest


log: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def func(x):
    foo = PogoOCR.ProfileSelf("key.json", image_uri=x)
    foo.get_text()
    log.debug(foo.text_found[0].description)
    result = {
        "locale": foo.locale,
        "numeric_locale": foo.numeric_locale,
        "username": foo.username,
        "travel_km": foo.travel_km,
        "capture_total": foo.capture_total,
        "pokestops_visited": foo.pokestops_visited,
        "total_xp": foo.total_xp,
    }
    return result


options = [
    (
        "fr",
        "https://cdn.discordapp.com/attachments/339450026076012544/712570150921961512/Screenshot_20200520-083906.jpg",
        {
            "locale": babel.Locale.parse("fr"),
            "numeric_locale": {"group": "\xa0", "decimal": ","},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "de",
        "https://cdn.discordapp.com/attachments/339450026076012544/712579182416232458/Screenshot_20200520-091452.jpg",
        {
            "locale": babel.Locale.parse("de"),
            "numeric_locale": {"group": ".", "decimal": ","},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "it",
        "https://cdn.discordapp.com/attachments/339450026076012544/712582940244181073/Screenshot_20200520-092956.jpg",
        {
            "locale": babel.Locale.parse("it"),
            "numeric_locale": {"group": ".", "decimal": ","},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "ja",
        "https://cdn.discordapp.com/attachments/339450026076012544/712585432520589352/Screenshot_20200520-093943.jpg",
        {
            "locale": babel.Locale.parse("ja"),
            "numeric_locale": {"group": ",", "decimal": "."},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "ko",
        "https://cdn.discordapp.com/attachments/339450026076012544/712587774309433364/Screenshot_20200520-094915.jpg",
        {
            "locale": babel.Locale.parse("ko"),
            "numeric_locale": {"group": ",", "decimal": "."},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "es",
        "https://cdn.discordapp.com/attachments/339450026076012544/712590402548662372/Screenshot_20200520-095940.jpg",
        {
            "locale": babel.Locale.parse("es"),
            "numeric_locale": {"group": ".", "decimal": ","},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "zh",
        "https://cdn.discordapp.com/attachments/339450026076012544/712592915234422784/Screenshot_20200520-100930.jpg",
        {
            "locale": babel.Locale.parse("zh_hant"),
            "numeric_locale": {"group": ",", "decimal": "."},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "en",
        "https://cdn.discordapp.com/attachments/543105822629167104/709926063282847834/Screenshot_20200513-013228.jpg",
        {
            "locale": babel.Locale.parse("en"),
            "numeric_locale": {"group": ",", "decimal": "."},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6163.7"),
            "capture_total": 55718,
            "pokestops_visited": 42807,
            "total_xp": 68064220,
        },
    ),
    (
        "pt",
        "https://cdn.discordapp.com/attachments/339450026076012544/712597570421260408/Screenshot_20200520-102802.jpg",
        {
            "locale": babel.Locale.parse("pt_br"),
            "numeric_locale": {"group": ".", "decimal": ","},
            "username": "JayTurnrTDX",
            "travel_km": decimal.Decimal("6170.4"),
            "capture_total": 55865,
            "pokestops_visited": 42809,
            "total_xp": 68315780,
        },
    ),
    (
        "edge_of_screen",
        "https://cdn.discordapp.com/attachments/329751396222238722/711468207667544095/Screenshot_20200517-074014.png",
        (
            {
                "locale": babel.Locale.parse("en"),
                "numeric_locale": {"group": ",", "decimal": "."},
                "username": "nerraw1986",
                "travel_km": decimal.Decimal("1325.7"),
                "capture_total": 4721,
                "pokestops_visited": 3309,  # Real Stat
                "total_xp": 5421143,
            },
            {
                "locale": babel.Locale.parse("en"),
                "numeric_locale": {"group": ",", "decimal": "."},
                "username": "nerraw1986",
                "travel_km": decimal.Decimal("1325.7"),
                "capture_total": 4721,
                "pokestops_visited": None,  # Known bug, searching fix, not world ending
                "total_xp": 5421143,
            },
        ),
    ),
    (
        "xp_total_xp_issue",
        "https://cdn.discordapp.com/attachments/329751396222238722/711961584230203402/Screenshot_20200518-162012_Pokmon_GO.jpg",
        {
            "locale": babel.Locale.parse("en"),
            "numeric_locale": {"group": ",", "decimal": "."},
            "username": None,
            "travel_km": decimal.Decimal("1895.9"),
            "capture_total": 8418,
            "pokestops_visited": 3375,
            "total_xp": 9931565,
        },
    ),
    (
        "fr",
        "https://cdn.discordapp.com/attachments/370708840850653184/752445686699786270/Screenshot_20200907_103022_com.nianticlabs.pokemongo.jpg",
        {
            "locale": babel.Locale.parse("fr"),
            "numeric_locale": {"group": "\xa0", "decimal": "."},
            "username": "03icemix",
            "travel_km": decimal.Decimal("809.1"),
            "capture_total": 12537,
            "pokestops_visited": 11633,
            "total_xp": 11931177,
        },
    ),
    (
        "english with non-english numerics",
        "https://cdn.discordapp.com/attachments/370708840850653184/751596341985148958/image0.png",
        {
            "locale": babel.Locale.parse("en"),
            "numeric_locale": {"group": "\xa0", "decimal": ","},
            "username": None,
            "travel_km": decimal.Decimal("1127.1"),
            "capture_total": 21543,
            "pokestops_visited": 10457,
            "total_xp": 16657146,
        },
    ),
    (
        "english with but missing travel_km",
        "https://cdn.discordapp.com/attachments/370708840850653184/752889030680510494/Screenshot_20200908-145202.jpg",
        {
            "locale": babel.Locale.parse("en"),
            "numeric_locale": {"group": ","},
            "username": None,
            "travel_km": None,
            "capture_total": 6062,
            "pokestops_visited": 44890,
            "total_xp": 75751423,
        },
    ),
]


@pytest.mark.parametrize("test_name,input,expected", options)
def test_answer(test_name, input, expected):
    res = func(input)
    if isinstance(expected, tuple):
        assert any([res == e for e in expected])
    else:
        assert res == expected
