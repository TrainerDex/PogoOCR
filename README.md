[![Support Server](https://img.shields.io/discord/614101299197378571.svg?color=7289da&label=Support&logo=discord&style=flat)](https://discord.gg/pdxh7P)
[![PyPi version](https://badgen.net/pypi/v/PogoOCR/)](https://pypi.com/project/PogoOCR)
[![Maintenance](https://img.shields.io/static/v1?label=Maintained?&message=yes&color=success&style=flat)](#)
[![wakatime](https://wakatime.com/badge/github/TrainerDex/PogoOCR.svg?style=flat)](https://wakatime.com/badge/github/TrainerDex/PogoOCR)
[![codecov](https://codecov.io/gh/TrainerDex/PogoOCR/branch/develop/graph/badge.svg?token=LABKE6I5RL)](https://codecov.io/gh/TrainerDex/PogoOCR)

A Python tool for running OCR on Pokémon Screenshots using Google Cloud Vision


Usage:

```py
import PogoOCR
from google.oauth2 import service_account

credentials: service_account.Credentials

client = PogoOCR.OCRClient(credentials=credentials)
screenshot = PogoOCR.Screenshot.from_url(
    url="...",
    klass=PogoOCR.ScreenshotClass.ACTIVITY_VIEW,
)

request = client.open_request(screenshot, PogoOCR.Language.ENGLISH)

result = client.process_ocr(request)
```
