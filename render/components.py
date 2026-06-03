import math
from PIL import ImageFont

from config import FONT_BOLD


WMO_SYMBOL = {
    0: "☀",
    1: "⛅",
    2: "⛅",
    3: "☁",
    45: "≋",
    48: "≋",
    51: "☔",
    53: "☔",
    55: "☔",
    56: "☔",
    57: "☔",
    61: "☔",
    63: "☔",
    65: "☔",
    66: "☔",
    67: "☔",
    71: "❄",
    73: "❄",
    75: "❄",
    77: "❄",
    80: "☔",
    81: "☔",
    82: "☔",
    85: "❄",
    86: "❄",
    95: "⚡",
    96: "⚡",
    99: "⚡",
}


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_chip(draw, xy, text, font):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + 6, y0, x1 - 6, y1], fill=0)
    draw.ellipse([x0, y0, x0 + 12, y1], fill=0)
    draw.ellipse([x1 - 12, y0, x1, y1], fill=0)

    text_width = draw.textlength(text, font=font)
    draw.text(
        (x0 + (x1 - x0 - text_width) / 2, y0 + (y1 - y0 - font.size) / 2 - 1),
        text,
        font=font,
        fill=255,
    )


def wrap_text(draw, text, font, max_width):
    if draw.textlength(text, font=font) <= max_width:
        return [text, ""]

    words = text.split()
    if not words:
        return ["", ""]

    line1 = words.pop(0)
    for word in words:
        if draw.textlength(line1 + " " + word, font=font) <= max_width:
            line1 += " " + word
        else:
            break

    line2 = text[len(line1):].lstrip()
    return [line1, line2]


def shorten_middle(text, maxlen=18):
    if len(text) <= maxlen:
        return text
    return text[:maxlen].rstrip() + "…"


def hhmm(value):
    import datetime

    try:
        return datetime.datetime.fromisoformat(value).strftime("%H:%M")
    except Exception:
        return "--:--"