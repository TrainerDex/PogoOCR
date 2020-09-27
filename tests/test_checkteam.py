import babel
import decimal
import logging
import PogoOCR
import pytest


log: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

TEAMLESS = 0
MYSTIC = 1
VALOR = 2
INSTINCT = 3


def func(x):
    foo = PogoOCR.ProfileSelf("key.json", image_uri=x)
    result = foo.get_team()
    return result


options = [
    (
        "https://cdn.discordapp.com/attachments/339450026076012544/712570150921961512/Screenshot_20200520-083906.jpg",
        VALOR,
    ),
    (
        "https://cdn.discordapp.com/attachments/329751396222238722/711468207667544095/Screenshot_20200517-074014.png",
        VALOR,
    ),
    (
        "https://cdn.discordapp.com/attachments/329751396222238722/711961584230203402/Screenshot_20200518-162012_Pokmon_GO.jpg",
        INSTINCT,
    ),
    (
        "https://cdn.discordapp.com/attachments/370708840850653184/752445686699786270/Screenshot_20200907_103022_com.nianticlabs.pokemongo.jpg",
        INSTINCT,
    ),
    (
        "https://cdn.discordapp.com/attachments/370708840850653184/751596341985148958/image0.png",
        VALOR,
    ),
    (
        "https://cdn.discordapp.com/attachments/370708840850653184/752889030680510494/Screenshot_20200908-145202.jpg",
        VALOR,
    ),
    (
        "https://cdn.discordapp.com/attachments/534176124025044992/759864766453121064/image0.png",
        TEAMLESS,
    ),
    (
        "https://cdn.discordapp.com/attachments/426869945628884992/752665941023653928/image0.png",
        INSTINCT,
    ),
    (
        "https://cdn.discordapp.com/attachments/329751396222238722/636564323552067615/Screenshot_20191023-145907.jpg",
        MYSTIC,
    ),
    (
        "https://cdn.discordapp.com/attachments/471278432265830400/759871374708703252/Screenshot_20200927-211709.jpg",
        None,
    ),
    (
        "https://cdn.discordapp.com/attachments/473936700905619487/476076434092326912/image.png",
        None,
    ),
]


@pytest.mark.parametrize("input,expected", options)
def test_answer(input, expected):
    res = func(input)
    assert res == expected
