"""
PokeOCR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python tool for running OCR on Pokemon Screenshots
"""

__title__ = "PogoOCR"
__author__ = "JayTurnr/DynamicalSystem"

import math
from PIL import Image


class PokeOCR:
    def __init__(self, pic):
        self.filename = pic
        self.update_pic = Image.open(self.filename)
        self.x, self.y = self.update_pic.size
        self.res = "{}x{}".format(self.x, self.y)
        self.team_guess = self.__guess_team(self.update_pic)

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
