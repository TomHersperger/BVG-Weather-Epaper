from render.components import WMO_SYMBOL, hhmm


def first(values, default=None):
    return values[0] if values else default


def draw_current_weather(draw, current, daily, x, y, fonts):
    icon_font = fonts["weather_icon"]
    temp_font = fonts["bold_68"]
    main_font = fonts["bold_26"]
    text_font = fonts["regular_22"]

    code = int(current.get("weather_code") or 0)
    icon = WMO_SYMBOL.get(code, "☁")

    current_temp = current.get("temperature_2m")
    min_temp = first(daily.get("temperature_2m_min") or [])
    max_temp = first(daily.get("temperature_2m_max") or [])
    feels_like = current.get("apparent_temperature")
    wind = current.get("wind_speed_10m")
    humidity = current.get("relative_humidity_2m")
    sunrise = first(daily.get("sunrise") or [])
    sunset = first(daily.get("sunset") or [])

    current_y = y

    if current_temp is not None:
        icon_width = draw.textlength(icon, font=icon_font)
        draw.text((x, current_y + 10), icon, font=icon_font, fill=0)
        draw.text(
            (x + icon_width + 12, current_y),
            f"{current_temp:.0f}°C",
            font=temp_font,
            fill=0,
        )
        current_y += 78

    if min_temp is not None and max_temp is not None:
        draw.text(
            (x, current_y),
            f"min {min_temp:.0f}° / max {max_temp:.0f}°",
            font=main_font,
            fill=0,
        )
        current_y += 34

    if feels_like is not None:
        draw.text(
            (x, current_y),
            f"fühlt sich an wie {feels_like:.0f}°",
            font=main_font,
            fill=0,
        )
        current_y += 32

    parts = []
    if wind is not None:
        parts.append(f"Wind {wind:.0f} km/h")
    if humidity is not None:
        parts.append(f"Feuchte {humidity:.0f}%")

    if parts:
        draw.text((x, current_y), "  •  ".join(parts), font=text_font, fill=0)
        current_y += 30

    if sunrise and sunset:
        draw.text(
            (x, current_y),
            f"↑ {hhmm(sunrise)}    •    ↓ {hhmm(sunset)}",
            font=text_font,
            fill=0,
        )
