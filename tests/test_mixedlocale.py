import PogoOCR
import pprint as pp
import pytest


def func(x):
    foo = PogoOCR.ProfileSelf("key.json", image_uri=x)
    foo.get_text()
    pp.pprint(foo.__dict__)
    return (foo.locale, foo.number_locale)


options = [
    (
        "en_,.",
        "https://cdn.discordapp.com/attachments/543105822629167104/709926063282847834/Screenshot_20200513-013228.jpg",
        ("en", ",."),
    ),
    (
        "fr_ .",
        "https://cdn.discordapp.com/attachments/370708840850653184/752445686699786270/Screenshot_20200907_103022_com.nianticlabs.pokemongo.jpg",
        ("fr", " ."),
    ),
    (
        "en_ ,",
        "https://cdn.discordapp.com/attachments/370708840850653184/751596341985148958/image0.png",
        ("en", " ,"),
    ),
]


@pytest.mark.parametrize("test_name,input,expected", options)
def test_answer(test_name, input, expected):
    assert func(input) == expected
