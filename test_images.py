import PogoOCR

def func(x):
    foo = PogoOCR.ProfileSelf('key.json', image_uri=x)
    foo.get_text()
    foo.find_stats()
    return foo.total_xp

def test_answer():
    assert func('https://cdn.discordapp.com/attachments/543105822629167104/709926063282847834/Screenshot_20200513-013228.jpg') == 68064220
