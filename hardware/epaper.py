import os
import sys
import time


def get_epaper_driver():
    try:
        from waveshare_epd import epd7in5_V2
        return epd7in5_V2
    except ImportError:
        candidates = [
            os.path.expanduser("~/e-Paper/RaspberryPi_JetsonNano/python/lib"),
        ]

        for candidate in candidates:
            if os.path.isdir(candidate):
                sys.path.append(candidate)
                try:
                    from waveshare_epd import epd7in5_V2
                    return epd7in5_V2
                except ImportError:
                    pass

    return None


def display_or_save_preview(img, epd_driver, cycle, full_clear_every):
    out_dir = os.path.join(os.getcwd(), "tmp")
    os.makedirs(out_dir, exist_ok=True)

    if not epd_driver:
        out = os.path.join(out_dir, "epaper_preview.png")
        img.save(out)
        print(f"Saved preview -> {out}")
        return

    try:
        epd = epd_driver.EPD()
        epd.init()

        if full_clear_every and cycle % full_clear_every == 0:
            epd.Clear()

        epd.display(epd.getbuffer(img))
        time.sleep(2)
        epd.sleep()

        print(f"[{time.strftime('%H:%M:%S')}] Display updated (cycle {cycle})")

    except Exception as e:
        print("E-paper render failed, saving preview instead:", e)
        out = os.path.join(out_dir, "epaper_preview.png")
        img.save(out)
        print(f"Saved preview -> {out}")