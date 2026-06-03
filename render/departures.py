from config import EPD_WIDTH, EPD_HEIGHT
from render.components import draw_chip, wrap_text, shorten_middle
from services.bvg import format_prod


CHIP_WIDTH = 56
CHIP_HEIGHT = 20


def draw_departures(draw, stops, departures_by_stop, x, y, fonts):
    stop_font = fonts["bold_24"]
    empty_font = fonts["regular_16"]
    badge_font = fonts["regular_16"]
    dest_font = fonts["regular_18"]
    mins_font = fonts["bold_20"]

    current_y = y

    for stop in stops:
        draw.text((x, current_y), stop["name"], font=stop_font, fill=0)
        current_y += 30

        departures = departures_by_stop.get(stop["id"], [])

        if not departures:
            draw.text((x, current_y), "No upcoming departures", font=empty_font, fill=0)
            current_y += 24

        for departure in departures[: stop.get("limit", 4)]:
            current_y = draw_departure_row(
                draw=draw,
                departure=departure,
                x=x,
                y=current_y,
                badge_font=badge_font,
                dest_font=dest_font,
                mins_font=mins_font,
            )

        current_y += 4
        draw.line((x, current_y, EPD_WIDTH - 16, current_y), fill=0)
        current_y += 10

        if current_y > EPD_HEIGHT - 26:
            break


def draw_departure_row(draw, departure, x, y, badge_font, dest_font, mins_font):
    badge = build_badge(departure)

    draw_chip(draw, (x, y - 2, x + CHIP_WIDTH, y - 2 + CHIP_HEIGHT), badge, badge_font)

    dest_max_width = EPD_WIDTH - 20 - (x + CHIP_WIDTH + 10) - 90
    short_dest = shorten_middle(departure["dest"], 18)
    line1, line2 = wrap_text(draw, short_dest, dest_font, dest_max_width)

    draw.text((x + CHIP_WIDTH + 10, y - 2), line1, font=dest_font, fill=0)
    if line2:
        draw.text((x + CHIP_WIDTH + 10, y + 16), line2, font=dest_font, fill=0)

    minutes_text = build_minutes_text(departure)
    minutes_width = draw.textlength(minutes_text, font=mins_font)
    draw.text((EPD_WIDTH - 16 - minutes_width, y - 4), minutes_text, font=mins_font, fill=0)

    return y + (22 if not line2 else 34)


def build_badge(departure):
    product = format_prod(departure["prod"])
    line = departure["line"]
    if product and not line.startswith(product):
        return f"{product}{line}"
    return line


def build_minutes_text(departure):
    text = f"{departure['mins']} min"
    if departure["delay_min"]:
        text += f" (+{departure['delay_min']})"
    return text
