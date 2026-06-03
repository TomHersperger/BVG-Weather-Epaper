# Raspberry Pi E-Paper Dashboard

A lightweight dashboard for a Raspberry Pi with a Waveshare 7.5" E-Paper Display.

It shows current weather, rain probability, a short weather forecast, and public transport departures using BVG/VBB data.

The project is designed for an 800×480 px E-Paper Display, such as the Waveshare 7.5" V2.

## Features

* Current weather via Open-Meteo
* Temperature, feels-like temperature, wind, and humidity
* Sunrise and sunset
* Rain probability for the next few hours
* Maximum rain probability for today
* Weather forecast for the next days
* Configurable BVG/VBB departure stops
* Optional line filters per stop
* Automatic refresh loop
* Preview image fallback if no E-Paper driver is available
* Optional autostart with systemd

## Hardware Requirements

* Raspberry Pi
* microSD card with Raspberry Pi OS
* Waveshare 7.5" E-Paper Display, 800×480 px
* Internet connection
* Raspberry Pi power supply

## Project Structure

Example structure:

```text
e-paper-dashboard/
├── bvg_weather_epaper.py
├── config.py
├── fonts/
│   ├── DejaVuLGCSans.ttf
│   └── DejaVuLGCSans-Bold.ttf
├── hardware/
│   ├── __init__.py
│   └── epaper.py
├── render/
│   ├── __init__.py
│   ├── components.py
│   ├── dashboard.py
│   ├── topbar.py
│   ├── current_weather.py
│   ├── rain_summary.py
│   ├── week_forecast.py
│   └── departures.py
├── services/
│   ├── __init__.py
│   ├── bvg.py
│   └── weather.py
└── tmp/
    └── epaper_preview.png
```

## Installation

### 1. Install system packages

```bash
sudo apt update
sudo apt install -y git python3-pip python3-pil python3-numpy python3-requests python3-spidev python3-rpi.gpio python3-lgpio
```

### 2. Enable SPI

The Waveshare E-Paper Display uses SPI.

```bash
sudo raspi-config
```

Then enable:

```text
Interface Options → SPI → Enable
```

Reboot afterwards:

```bash
sudo reboot
```

Check that SPI is available:

```bash
ls /dev/spidev*
```

Expected output:

```text
/dev/spidev0.0  /dev/spidev0.1
```

### 3. Install the Waveshare E-Paper library

The project expects the Waveshare library at:

```text
~/e-Paper/RaspberryPi_JetsonNano/python/lib
```

Install it with:

```bash
cd ~
git clone https://github.com/waveshareteam/e-Paper.git
```

If the folder already exists:

```bash
cd ~/e-Paper
git pull
```

Test the driver:

```bash
python -c "import sys, os; sys.path.append(os.path.expanduser('~/e-Paper/RaspberryPi_JetsonNano/python/lib')); from waveshare_epd import epd7in5_V2; print('Driver OK')"
```

If `Driver OK` appears, the driver can be imported.

### 4. Clone this project

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

Run the dashboard:

```bash
python bvg_weather_epaper.py
```

If the display driver is not available, the script saves a preview image instead:

```text
tmp/epaper_preview.png
```

## Configuration

Most settings are stored in `config.py`.

Example:

```python
LAT = 52.5200
LON = 13.4050
LOCATION_NAME = "Berlin"

UPDATE_EVERY_SEC = 180
FULL_CLEAR_EVERY = 10

VBB_BASE = "https://v6.vbb.transport.rest"
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
TZ = "Europe/Berlin"
```

### Weather location

Change the coordinates and display name:

```python
LAT = 52.5200
LON = 13.4050
LOCATION_NAME = "Berlin"
```

Example for another city:

```python
LAT = 48.1374
LON = 11.5755
LOCATION_NAME = "Munich"
```

## Adding or changing public transport stops

Stops are configured in `config.py` in the `STOPS` list.

Example:

```python
STOPS = [
    {"id": "900100003", "name": "Example Stop", "limit": 2, "lines": None},
    {"id": "900100004", "name": "Example Station", "limit": 2, "lines": ["U1"]},
    {"id": "900100005", "name": "Example S-Bahn", "limit": 4, "lines": ["S"]},
    {"id": "900100006", "name": "Example Bus Stop", "limit": 4, "lines": ["100", "200"]},
]
```

### Stop configuration fields

```python
{
    "id": "900100004",
    "name": "Example Station",
    "limit": 2,
    "lines": ["U1"]
}
```

* `id`: BVG/VBB stop ID
* `name`: Name displayed on the E-Paper
* `limit`: Maximum number of departures shown
* `lines`: Optional line filter, or `None`

### Examples

Show all lines for a stop:

```python
{"id": "900100003", "name": "Example Stop", "limit": 2, "lines": None}
```

Show only one specific line:

```python
{"id": "900100004", "name": "Example Station", "limit": 2, "lines": ["U1"]}
```

Show only S-Bahn lines:

```python
{"id": "900100005", "name": "Example S-Bahn", "limit": 4, "lines": ["S"]}
```

Show only selected bus lines:

```python
{"id": "900100006", "name": "Example Bus Stop", "limit": 4, "lines": ["100", "200"]}
```

## Finding a stop ID

Stop IDs can be searched through the transport.rest API.

Open this in a browser:

```text
https://v6.vbb.transport.rest/locations?query=Alexanderplatz&results=5&pretty=true
```

Or use `curl`:

```bash
curl "https://v6.vbb.transport.rest/locations?query=Alexanderplatz&results=5&pretty=true"
```

Find the matching station or stop in the response and use its `id` in `config.py`.

## Testing the API

Test departures for a stop in the browser:

```text
https://v6.vbb.transport.rest/stops/900100003/departures?duration=30&results=4&pretty=true
```

Alternative endpoint:

```text
https://v6.bvg.transport.rest/stops/900100003/departures?duration=30&results=4&pretty=true
```

If the API works, it returns JSON data.

If you see `503 Service Unavailable` or a timeout, the external API may be temporarily unavailable.

## Clearing the E-Paper Display

To clear the display manually:

```bash
python -c "import sys, os; sys.path.append(os.path.expanduser('~/e-Paper/RaspberryPi_JetsonNano/python/lib')); from waveshare_epd import epd7in5_V2; epd=epd7in5_V2.EPD(); epd.init(); epd.Clear(); epd.sleep(); print('cleared')"
```

If `GPIO busy` appears, another process is already using the display.

Stop the service first if systemd is used:

```bash
sudo systemctl stop epaper.service
```

Or stop running dashboard processes:

```bash
sudo pkill -f bvg_weather_epaper.py
```

## Optional: Autostart with systemd

Create a service file:

```bash
sudo nano /etc/systemd/system/epaper.service
```

Example service:

```ini
[Unit]
Description=E-Paper BVG Weather Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=<USER>
WorkingDirectory=/home/<USER>/<PROJECT_FOLDER>
ExecStart=/usr/bin/python /home/<USER>/<PROJECT_FOLDER>/bvg_weather_epaper.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Replace:

```text
<USER>
<PROJECT_FOLDER>
```

with the correct values for your setup.

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable epaper.service
sudo systemctl start epaper.service
```

Check status:

```bash
sudo systemctl status epaper.service
```

View logs:

```bash
journalctl -u epaper.service -f
```

Restart after code changes:

```bash
sudo systemctl restart epaper.service
```

Stop the service:

```bash
sudo systemctl stop epaper.service
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'waveshare_epd'`

The Waveshare library was not found.

Check:

```bash
ls ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd
```

If the folder does not exist:

```bash
cd ~
git clone https://github.com/waveshareteam/e-Paper.git
```

### `GPIO busy`

Another process is using the GPIO pins.

Stop the service:

```bash
sudo systemctl stop epaper.service
```

Or stop running dashboard processes:

```bash
sudo pkill -f bvg_weather_epaper.py
```

### API timeout or HTTP 503

The external BVG/VBB API may be slow or temporarily unavailable.

Test in a browser:

```text
https://v6.vbb.transport.rest/stops/900100003/departures?duration=30&results=4&pretty=true
```

If this test also fails, the issue is probably not caused by the Raspberry Pi or the display.

### Only a preview image is saved

If the terminal shows:

```text
Saved preview -> tmp/epaper_preview.png
```

the E-Paper driver was not found or the display could not be accessed.

Test the driver:

```bash
python -c "import sys, os; sys.path.append(os.path.expanduser('~/e-Paper/RaspberryPi_JetsonNano/python/lib')); from waveshare_epd import epd7in5_V2; print('Driver OK')"
```

### Display still shows an old image

E-Paper displays keep showing the previous image even without power. This is normal.

Clear it manually:

```bash
python -c "import sys, os; sys.path.append(os.path.expanduser('~/e-Paper/RaspberryPi_JetsonNano/python/lib')); from waveshare_epd import epd7in5_V2; epd=epd7in5_V2.EPD(); epd.init(); epd.Clear(); epd.sleep(); print('cleared')"
```

## Notes

* Public transport data is provided through `transport.rest`.
* Weather data is provided through Open-Meteo.
* External APIs may be temporarily unavailable.
* Do not commit passwords, private SSH keys, Wi-Fi credentials, or local configuration secrets.
