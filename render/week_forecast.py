import datetime

from render.components import WMO_SYMBOL


DAYS_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def list_value(values, index, default=None):
    return values[index] if index < len(values) else default


def day_name_from_iso(date_text):
    try:
        date = datetime.datetime.fromisoformat(date_text)
        return DAYS_DE[date.weekday()]
    except Exception:
        return "?"


def draw_week_forecast(draw, daily, x, y, width, fonts):
    title_font = fonts["regular_22"]
    day_font = fonts["regular_18"]
    text_font = fonts["regular_18"]

    times = daily.get("time") or []
    codes = daily.get("weather_code") or []
    min_temps = daily.get("temperature_2m_min") or []
    max_temps = daily.get("temperature_2m_max") or []
    rain_probs = daily.get("precipitation_probability_max") or []

    if len(times) < 2:
        draw.text((x, y), "Wochenwetter nicht verfügbar", font=text_font, fill=0)
        return

    draw.text((x, y), "Nächste Tage", font=title_font, fill=0)
    draw.line((x, y + 26, x + width, y + 26), fill=0)

    start_y = y + 34
    row_h = 24

    # Start at 1: index 0 is today, index 1 is tomorrow.
    for day_index in range(1, min(6, len(times))):
        row_y = start_y + (day_index - 1) * row_h

        day_name = day_name_from_iso(times[day_index])

        code = int(list_value(codes, day_index, 3) or 0)
        icon = WMO_SYMBOL.get(code, "☁")

        min_temp = list_value(min_temps, day_index)
        max_temp = list_value(max_temps, day_index)
        rain = list_value(rain_probs, day_index)

        temp_text = "--/--"
        if min_temp is not None and max_temp is not None:
            temp_text = f"{min_temp:.0f}°/{max_temp:.0f}°"

        rain_text = "--"
        if rain is not None:
            rain_text = f"☔ {int(rain)}%"

        draw.text((x, row_y), day_name, font=day_font, fill=0)
        draw.text((x + 45, row_y), icon, font=day_font, fill=0)
        draw.text((x + 90, row_y), temp_text, font=text_font, fill=0)
        draw.text((x + 190, row_y), rain_text, font=text_font, fill=0)
