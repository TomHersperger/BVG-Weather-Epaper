import datetime


def rain_label(value):
    if value is None:
        return "--"
    if value >= 70:
        return "hoch"
    if value >= 35:
        return "mittel"
    if value > 0:
        return "gering"
    return "kein"


def next_hourly_rain_values(hourly, hours=4):
    times = hourly.get("time") or []
    probs = hourly.get("precipitation_probability") or []

    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    start_index = 0
    while start_index < len(times):
        try:
            hour = datetime.datetime.fromisoformat(times[start_index])
            if hour >= now:
                break
        except Exception:
            pass
        start_index += 1

    values = []
    for offset in range(hours):
        index = start_index + offset
        if index < len(probs):
            values.append(int(probs[index] or 0))

    return values


def draw_rain_summary(draw, daily, hourly, x, y, fonts):
    font = fonts["regular_18"]

    daily_rain = daily.get("precipitation_probability_max") or []
    today_max = int(daily_rain[0] or 0) if daily_rain else None

    next_probs = next_hourly_rain_values(hourly, hours=4)
    next_max = max(next_probs) if next_probs else None

    if next_max is None:
        line1 = "☔ Nächste 4h: --"
    else:
        line1 = f"☔ Nächste 4h: {rain_label(next_max)} ({next_max}%)"

    today_text = f"{today_max}%" if today_max is not None else "--"
    line2 = f"☔ Heute max: {today_text}"

    draw.text((x, y), line1, font=font, fill=0)
    draw.text((x, y + 24), line2, font=font, fill=0)
