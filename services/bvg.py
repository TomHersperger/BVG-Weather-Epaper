import datetime
import requests

from config import VBB_BASE, REQUEST_TIMEOUT

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "bvg-epaper/1.0"
})


def _fetch_departures_core(kind, stop_id, minutes=60, limit=20):
    params = {
        "duration": str(minutes),
        "results": str(limit),
        "pretty": "false",
    }

    url = f"{VBB_BASE}/{kind}/{stop_id}/departures"
    response = SESSION.get(url, params=params, timeout=REQUEST_TIMEOUT)

    if response.status_code == 404:
        return {}

    response.raise_for_status()
    return response.json()


def fetch_departures(stop_cfg, minutes=60, limit=20):
    stop_id = stop_cfg["id"]

    data = _fetch_departures_core("stops", stop_id, minutes, limit * 3)
    if not data:
        data = _fetch_departures_core("stations", stop_id, minutes, limit * 3)

    departures = []
    for item in data.get("departures", []):
        if not isinstance(item, dict):
            continue

        line_info = item.get("line") or {}
        line = line_info.get("name", "?")
        prod = line_info.get("product") or ""
        dest = (item.get("direction") or "").replace(" (Berlin)", "")
        when = item.get("when") or item.get("plannedWhen")

        if not when:
            continue

        try:
            dt = datetime.datetime.fromisoformat(when)
            now = datetime.datetime.now(dt.tzinfo)
            mins = int(round((dt - now).total_seconds() / 60.0))
        except Exception:
            continue

        delay_sec = item.get("delay") or 0

        if mins < 0:
            continue
        if prod == "suburban" and mins < 1:
            continue
        if prod == "bus" and mins < 1:
            continue

        departures.append({
            "line": line,
            "dest": dest,
            "mins": mins,
            "prod": prod,
            "delay_min": int(round(delay_sec / 60)) if delay_sec else 0,
        })

    departures.sort(key=lambda x: x["mins"])
    departures = _filter_lines(departures, stop_cfg.get("lines"))

    return departures[:stop_cfg.get("limit", limit)]


def _filter_lines(departures, lines):
    if not lines:
        return departures

    if len(lines) == 1 and lines[0] in ["S", "U", "B", "T", "F"]:
        prefix = lines[0]
        return [d for d in departures if d["line"].startswith(prefix)]

    return [d for d in departures if d["line"] in lines]


def format_prod(prod):
    mapping = {
        "subway": "U",
        "suburban": "S",
        "tram": "T",
        "bus": "B",
        "ferry": "F",
        "express": "IC",
        "regional": "RE",
    }
    return mapping.get(prod or "", "")
