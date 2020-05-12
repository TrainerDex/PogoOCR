"""
PogoOCR for TL40
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python tool for running OCR on Pokemon Screenshots using Google Cloud Vision
Forked for TL40 specific purposes

:copyright: (c) 2018 TrainerDex
:licence: GNU GENERAL PUBLIC LICENSE 3.0

"""

__title__ = 'PogoOCR'
__author__ = 'JayTurnr'
__licence__ = 'GNU GENERAL PUBLIC LICENSE 3.0'
__copyright__ = '2018 TrainerDex'
__version__ = '0.1.0'

from .cloudvision import Image
from .types import ProfileTop, ProfileBottom, Badge, Pokédex
