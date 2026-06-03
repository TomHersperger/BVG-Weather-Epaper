import datetime

from config import EPD_WIDTH, TOPBAR_H, LOCATION_NAME


def draw_topbar(draw, fonts):
    now = datetime.datetime.now()

    left_text = now.strftime("%a %d %b %Y")
    title = f"{LOCATION_NAME} • BVG & Weather"
    right_text = "Last update " + now.strftime("%H:%M")

    date_font = fonts["regular_16"]
    title_font = fonts["bold_22"]

    draw.rectangle([0, 0, EPD_WIDTH, TOPBAR_H], fill=0)

    draw.text((12, TOPBAR_H // 2 - 9), left_text, font=date_font, fill=255)

    title_width = draw.textlength(title, font=title_font)
    draw.text(
        ((EPD_WIDTH - title_width) // 2, TOPBAR_H // 2 - 12),
        title,
        font=title_font,
        fill=255,
    )

    right_width = draw.textlength(right_text, font=date_font)
    draw.text(
        (EPD_WIDTH - 12 - right_width, TOPBAR_H // 2 - 9),
        right_text,
        font=date_font,
        fill=255,
    )
