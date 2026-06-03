from PIL import Image, ImageDraw

from config import (
    EPD_WIDTH,
    EPD_HEIGHT,
    TOPBAR_H,
    LEFT_COL_W,
    RIGHT_X,
    FONT_REG,
    FONT_BOLD,
)
from render.components import load_font
from render.topbar import draw_topbar
from render.current_weather import draw_current_weather
from render.rain_summary import draw_rain_summary
from render.week_forecast import draw_week_forecast
from render.departures import draw_departures


LEFT_X = 24
CURRENT_WEATHER_Y = TOPBAR_H + 10
RAIN_SUMMARY_Y = 255
WEEK_FORECAST_Y = 310
DEPARTURES_Y = TOPBAR_H + 8


def build_fonts():
    """Load all fonts once per render and pass them to sub-renderers."""
    return {
        "regular_16": load_font(FONT_REG, 16),
        "regular_18": load_font(FONT_REG, 18),
        "regular_20": load_font(FONT_REG, 20),
        "regular_22": load_font(FONT_REG, 22),
        "bold_20": load_font(FONT_BOLD, 20),
        "bold_22": load_font(FONT_BOLD, 22),
        "bold_24": load_font(FONT_BOLD, 24),
        "bold_26": load_font(FONT_BOLD, 26),
        "bold_68": load_font(FONT_BOLD, 68),
        "weather_icon": load_font(FONT_BOLD, 40),
    }


def draw_dashboard(stops, departures_by_stop, weather):
    img = Image.new("1", (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(img)
    fonts = build_fonts()

    current = weather.get("current", {}) or {}
    daily = weather.get("daily", {}) or {}
    hourly = weather.get("hourly", {}) or {}

    draw_topbar(draw, fonts)

    draw_current_weather(
        draw=draw,
        current=current,
        daily=daily,
        x=LEFT_X,
        y=CURRENT_WEATHER_Y,
        fonts=fonts,
    )

    draw_rain_summary(
        draw=draw,
        daily=daily,
        hourly=hourly,
        x=LEFT_X,
        y=RAIN_SUMMARY_Y,
        fonts=fonts,
    )

    draw_week_forecast(
        draw=draw,
        daily=daily,
        x=LEFT_X,
        y=WEEK_FORECAST_Y,
        width=LEFT_COL_W - 40,
        fonts=fonts,
    )

    draw_departures(
        draw=draw,
        stops=stops,
        departures_by_stop=departures_by_stop,
        x=RIGHT_X,
        y=DEPARTURES_Y,
        fonts=fonts,
    )

    return img
