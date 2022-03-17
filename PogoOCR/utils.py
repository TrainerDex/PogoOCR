from typing import Union
from colour import Color
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def calculate_colour_distance(c1: Color, c2: Color) -> float:
    """Users Delta E Cie 2000 to calculate colour distance

    Args:
        c1 (Color): First Colour
        c2 (Color): Second Colour

    Returns:
        float: Float distance between the two colours, 0 being the same colour, 100 being the furthest away, rounded to 3 decimal places
    """
    c1_lab = convert_color(sRGBColor(*c1.rgb), LabColor)
    c2_lab = convert_color(sRGBColor(*c2.rgb), LabColor)
    return round(delta_e_cie2000(c1_lab, c2_lab), 3)


def rgb2color(r: Union[int, float], g: Union[int, float], b: Union[int, float]) -> Color:
    r_float = r / 255
    g_float = g / 255
    b_float = b / 255
    return Color(rgb=(r_float, g_float, b_float))
