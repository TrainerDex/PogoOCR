import PogoOCR
import pytest

def func(x):
	foo = PogoOCR.ProfileSelf('key.json', image_uri=x)
	foo.get_text()
	print(foo.__dict__)
	return foo.total_xp

options = [
	('fr','https://cdn.discordapp.com/attachments/339450026076012544/712570150921961512/Screenshot_20200520-083906.jpg',68315780),
	('de','https://cdn.discordapp.com/attachments/339450026076012544/712579182416232458/Screenshot_20200520-091452.jpg',68315780),
	('it','https://cdn.discordapp.com/attachments/339450026076012544/712582940244181073/Screenshot_20200520-092956.jpg',68315780),
	('ja','https://cdn.discordapp.com/attachments/339450026076012544/712585432520589352/Screenshot_20200520-093943.jpg',68315780),
	('ko','https://cdn.discordapp.com/attachments/339450026076012544/712587774309433364/Screenshot_20200520-094915.jpg',68315780),
	('es','https://cdn.discordapp.com/attachments/339450026076012544/712590402548662372/Screenshot_20200520-095940.jpg',68315780),
	('zh_hant','https://cdn.discordapp.com/attachments/339450026076012544/712592915234422784/Screenshot_20200520-100930.jpg',68315780),
	('en','https://cdn.discordapp.com/attachments/543105822629167104/709926063282847834/Screenshot_20200513-013228.jpg',68064220),
	('pt_br','https://cdn.discordapp.com/attachments/339450026076012544/712597570421260408/Screenshot_20200520-102802.jpg',68315780),
	('edge_of_screen','https://cdn.discordapp.com/attachments/329751396222238722/711468207667544095/Screenshot_20200517-074014.png',5421143),
	('xp_total_xp_issue','https://cdn.discordapp.com/attachments/329751396222238722/711961584230203402/Screenshot_20200518-162012_Pokmon_GO.jpg',9931565), # This is the issue being fixed, leaving this test incase I break it in future
]

@pytest.mark.parametrize("test_name,input,expected", options)
def test_answer(test_name,input,expected):
	assert func(input) == expected
