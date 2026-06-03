import os

# Your location (used for nearby stops + weather). Berlin Mitte example:
LAT = 52.3110
LON = 13.2424
LOCATION_NAME = "Berlin"

# --- Update & refresh policy ---
UPDATE_EVERY_SEC = 180       # refresh every 3 minutes
FULL_CLEAR_EVERY = 10        # do a full clear every N cycles (reduces ghosting)
NETWORK_TIMEOUT   = 12       # requests timeout seconds

REQUEST_TIMEOUT = 10

STOPS = [
    {"id": "900100003", "name": "Example Stop", "limit": 2, "lines": None},
    {"id": "900100004", "name": "Example Station", "limit": 2, "lines": ["U1"]},
]

# Appearance (bigger)
HERE = os.path.dirname(__file__)
FONT_REG  = os.path.join(HERE, "fonts", "DejaVuLGCSans.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "DejaVuLGCSans-Bold.ttf")

# --- Layout / fonts ---
EPD_WIDTH = 800 
EPD_HEIGHT = 480
TOPBAR_H = 40           
LEFT_COL_W = 340     
RIGHT_X = LEFT_COL_W + 20


# APIs
VBB_BASE = "https://v6.vbb.transport.rest"
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
TZ = "Europe/Berlin"
