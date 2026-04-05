
![](images/tengwar_script.png)
> The Tengwar `(TENG-wahr)` script is an artificial script, one of several scripts created by J. R. R. Tolkien, the author of *The Lord of the Rings*. Within the context of Tolkien's fictional world, the Tengwar were invented by the Elf Fëanor, and used first to write the Elvish languages Quenya and Telerin.
>
> — [*Source*](https://en.wikipedia.org/wiki/Tengwar)
---

I'm building a wall mountable XY-plotter that draws my monthly calendar, updates events as they're added, and sometimes doodles baby Balrogs! Wouldn't it be cool to bring something from our digital space into our physical reality? Better yet, what if this thing could actually serve a dual purpose of both *function* and *art*! 

*Please note that this README will be a living, breathing document until I finish :)*

---

## Get Started
### Python Environment
1. Make sure you have Python 3.11+ installed.
2. Create a virtual environment (UnixOS): `python3.11 -m venv .tengwar`
3. Activate it (UnixOS): `source .tengwar/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
 
### Google Calendar
5. Follow the [Google Calendar Integration](#google-calendar-integration) section below to set up your `credentials.json`
6. Create a `.env` file in the project root with your shared calendar IDs (see the Google Calendar section for details). See `.env.example`.
7. Run `sync-cal` once to trigger the OAuth browser flow and generate `token.json`. 
 
### Arduino Firmware
8. Follow the [Firmware](#firmware) section below to flash Marlin onto the Arduino Mega
 
### Running
9. Plug in the Arduino via USB 
10. Run `python3 src/main.py --debug` to confirm the serial port and connection
11. Run `python3 src/main.py --port <your_port>` to start

---
 
## Google Calendar Integration
 
Tengwar syncs events from Google Calendar using the Google Calendar API. Follow these steps to set up credentials:
 
### 1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Click the project dropdown → **New Project**
- Name it `Tengwar` and click **Create**
 
### 2. Enable the Google Calendar API
- In your project, go to **APIs & Services** -> **Library**
- Search for `Google Calendar API` -> click it -> **Enable**
 
### 3. Configure the OAuth Consent Screen
- Go to **APIs & Services** -> **OAuth consent screen**
- Choose **External** -> **Create**
- Fill in the app name (`Tengwar`) and your email for support and developer contact
- Skip scopes → **Save and Continue**
- Under **Test users**, add your Google account email
- **Save**
 
### 4. Create Credentials
- Go to **APIs & Services** → **Credentials**
- Click **+ Create Credentials** → **OAuth client ID**
- Application type: **Desktop app** (this is correct even though the app runs on a Pi — the one-time OAuth flow runs on a machine with a browser, and the saved `token.json` is used for all future headless runs)
- Name it `Tengwar` → **Create**
- Download the JSON file, rename it to `credentials.json`, and place it in the project root
 
### 5. Configure Calendar IDs
Create a `.env` file in the project root:
```
YOUR_CALENDAR_ID=your_shared_calendar_id_here
```
To find a calendar ID, temporarily call `list_calendars()` from `gcal.py` — it will print all accessible calendars and their IDs.
 
### 6. First Run Authentication
On first run of `sync-cal`, a browser window will open for you to log in and grant access. This generates `token.json` which is reused for all future runs, no browser needed after that.
 
---
 
## Firmware
 
The Arduino Mega 2560 runs [Marlin bugfix-2.1.x](https://github.com/MarlinFirmware/Marlin), configured for the RAMPS 1.4 shield.
 
### VS Code & PlatformIO
 
Marlin firmware is built and flashed using VSCode with two extensions:
    - [PlatformIO IDE](https://platformio.org/) — a professional embedded development environment that handles toolchains, libraries, and board targets. It replaces the Arduino IDE for more complex firmware projects and supports hundreds of boards out of the box.
    - [Auto Build Marlin](https://marlinfw.org/docs/basics/auto_build_marlin.html) — a Marlin-specific extension that automatically selects the correct PlatformIO build target based on your `Configuration.h` and provides one-click build and upload.
 
This setup is worth keeping in mind for any future project that involves custom firmware on Arduino-based boards — particularly anything using RAMPS, RAMBo, or similar 3D printer control boards where you need to modify and recompile Marlin from source.
 
### Building & Flashing
 
1. Clone the Marlin source: `git clone https://github.com/MarlinFirmware/Marlin.git`
2. Copy `firmware/Configuration.h` and `firmware/Configuration_adv.h` into `Marlin/Marlin/`
3. Open the Marlin folder in VS Code with the [PlatformIO](https://platformio.org/) and [Auto Build Marlin](https://marlinfw.org/docs/basics/auto_build_marlin.html) extensions installed
4. Plug in the Arduino Mega via USB
5. Click **Upload** in the Auto Build Marlin sidebar
 
---
 
## Running
 
```bash
# Basic run (defaults to system date, /dev/ttyACM0)
python src/main.py
 
# Specify serial port (Mac)
python src/main.py --port /dev/<your_serial_port>
 
# Specify serial port (Pi)
python src/main.py --port /dev/ttyACM0
 
# Draw next calendar from a specific month
python src/main.py --next-cal --month 4 --year 2026
 
# Sync Google Calendar events
python src/main.py --sync-cal
 
# Debug mode — lists serial ports, tests connection
python src/main.py --debug
```
 
---

## Prototyping
### Physical Design
![First Iteration](images/v1_physical.png)

### Circuit Design
![First Iteration](images/v1_circuit.png)

### UML
![First Iteration](images/V1TengwarUML.svg)

---

## Materials
### Core Compute & Control
- 1 x Raspberry Pi 4 Model B (4 GB RAM)
    - 1 x SD Card
    - 1 x USB A Data Cable
- 1 x Arduino 2650 R3
- 1 x RAMPS 1.4 Shield
    - 2 x A4988 Drivers

### Motion Control
- 2 × NEMA 17 Stepper Motors
- 2 × A4988 Stepper Driver Modules
- 2 x KW12-3 Limit Switches
<!-- - 1 x Servo motor

### Power
- 24/5V Buck Boost Converter
- 24V PSU
- C14 Female

### Mechanical
- Linear rails, rods, or belt system (XY motion)
- Timing belts and pulleys or lead screws
- Pen holder 
- Wall-mount frame or backboard
- Fasteners (M3/M4 screws, nuts, spacers)
-->