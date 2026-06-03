#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import time

from config import (
    LAT,
    LON,
    STOPS,
    UPDATE_EVERY_SEC,
    FULL_CLEAR_EVERY,
)

from services.bvg import fetch_departures
from services.weather import fetch_weather
from render.dashboard import draw_dashboard
from hardware.epaper import get_epaper_driver, display_or_save_preview


def main():
    epd_driver = get_epaper_driver()
    cycle = 0

    stop = {"flag": False}

    def handle_stop(*_):
        stop["flag"] = True

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    print(
        f"Starting loop: interval={UPDATE_EVERY_SEC}s, "
        f"full_clear_every={FULL_CLEAR_EVERY}"
    )

    while not stop["flag"]:
        cycle += 1

        # --- BVG / VBB departures ---
        departures_by_stop = {}

        for stop_cfg in STOPS:
            try:
                departures = fetch_departures(
                    stop_cfg,
                    minutes=60,
                    limit=20,
                )

                departures_by_stop[stop_cfg["id"]] = departures

                print(
                    f"{stop_cfg['name']} ({stop_cfg['id']}): "
                    f"{len(departures)} deps"
                )

            except Exception as e:
                print(
                    f"Fehler beim Abrufen der Abfahrten für "
                    f"{stop_cfg['name']}: {e}"
                )
                departures_by_stop[stop_cfg["id"]] = []

        # --- Weather ---
        try:
            weather = fetch_weather(LAT, LON)

        except Exception as e:
            print("Failed to fetch weather:", e, file=sys.stderr)
            weather = {
                "current": {},
                "daily": {},
                "hourly": {},
            }

        # --- Render image ---
        img = draw_dashboard(
            STOPS,
            departures_by_stop,
            weather,
        )

        # --- Display or preview ---
        display_or_save_preview(
            img=img,
            epd_driver=epd_driver,
            cycle=cycle,
            full_clear_every=FULL_CLEAR_EVERY,
        )

        # --- Sleep, but allow Ctrl+C / systemd stop ---
        for _ in range(UPDATE_EVERY_SEC):
            if stop["flag"]:
                break
            time.sleep(1)

    print("Stopped loop. Bye.")


if __name__ == "__main__":
    main()