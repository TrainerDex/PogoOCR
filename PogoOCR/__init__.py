"""
PokeOCR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python tool for running OCR on Pokemon Screenshots

:copyright: (c) 2018 DynamicalSystem
:licence: Undecided, ask permission before using.

"""

__title__ = "PogoOCR"
__author__ = "JayTurnr/DynamicalSystem"
__licence__ = None
__copyright__ = "Copyright 2018 DynamicalSystem"
__version__ = "0.0.0"

import math
import pyocr
import re
from PIL import Image
from pyocr import builders


class PokeOCR:
    def __init__(self, pic):
        self.filename = pic
        self.update_pic = Image.open(self.filename)
        self.x, self.y = self.update_pic.size
        self.res = "{}x{}".format(self.x, self.y)
        self.tool = self.__get_tesseract()
        self.team_guess = self.__guess_team(self.update_pic)
        self.stats = {}
        self.stats["crop"] = self.__crop_percentage("stats")
        self.words = self.__guess_text(self.stats["crop"])
        for x in self.words:
            search = re.search("([0-9](?:\ )?(?:\,)?(?:\.)?)+", x)
            if bool(search) == True:
                self.stats_guess = (
                    re.search("([0-9](?:\ )?(?:\,)?(?:\.)?)+", x)
                    .group()
                    .replace(",", "")
                    .replace(".", "")
                    .replace(" ", "")
                )

    def __get_tesseract(self):
        tools = pyocr.get_available_tools()

        if len(tools) == 0:
            print("No OCR tool found")
            self.stats_guess = None
            exit

        # TBH, IDK if tesseract is always [0]
        return tools[0]

    def __crop_absolute(self, pic, box):
        return pic.crop((box[0][0], box[0][1], box[1][0], box[1][1]))

    def __crop_percentage(self, box):
        return self.update_pic.crop(
            (
                int(self.x * self.__BOXES["{0}_tl_x".format(box)]),
                int(self.y * self.__BOXES["{0}_tl_y".format(box)]),
                int(self.x * self.__BOXES["{0}_br_x".format(box)]),
                int(self.y * self.__BOXES["{0}_br_y".format(box)]),
            )
        )

    def __guess_text(self, pic):
        text = self.tool.image_to_string(
            pic, lang="eng", builder=pyocr.builders.TextBuilder()
        )

        return text.splitlines()

    def __guess_word_boxes(self, pic):
        word_boxes = self.tool.image_to_string(
            pic, lang="eng", builder=pyocr.builders.WordBoxBuilder()
        )

        return word_boxes

    __BOXES = {
        "trainer_tl_x": 0.060,
        "trainer_tl_y": 0.086,
        "trainer_br_x": 0.600,
        "trainer_br_y": 0.200,
        "level_tl_x": 0.497,
        "level_tl_y": 0.587,
        "level_br_x": 0.606,
        "level_br_y": 0.628,
        "xp_tl_x": 0.154,
        "xp_tl_y": 0.648,
        "xp_br_x": 0.445,
        "xp_br_y": 0.670,
        "stats_tl_x": 0.056,
        "stats_tl_y": 0.500,
        "stats_br_x": 0.805,
        "stats_br_y": 0.927,
    }

    def __distance(self, c1, c2):
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    __COLOURS = (
        ("Valor", (255, 0, 0)),
        ("Mystic", (0, 5, 255)),
        ("Instinct", (255, 246, 0)),
    )

    def __guess_team(self, pic, print_diag=False, alg=2):
        if alg == 1:
            cropped_image = pic.crop((0, pic.size[1] / 2, 5, pic.size[1] / 2 + 10))
            h = cropped_image.histogram()
            r, g, b = [
                h[i : i + int(256)] for i in range(0, 768, 256)
            ]  # Splits the histogram for the image into red, green and blue
            rgb = tuple(
                [sum(i * w for i, w in enumerate(c)) / sum(c) for c in [r, g, b]]
            )  # averages the values of each colour and joins back into one tuple or floats
        elif alg == 2:
            h = pic.histogram()
            rgb = pic.getpixel((2, pic.size[1] / 2))[0:3]
        closest_colours = sorted(
            self.__COLOURS, key=lambda colour: self.__distance(colour[1], rgb)
        )
        if print_diag:
            print("Channels: " + str(int(len(h) / 256)))
            print("RGB: " + str(rgb))
            print("Guesses :" + str(closest_colours))
        best_guess = closest_colours[0][0]
        return best_guess
