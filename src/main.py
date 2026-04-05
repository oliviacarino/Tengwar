# Initialize 
# Via CLI -- draw next calendar, manually trigger calendar sync 
# Manually sync the calendar since changing the paper isn't automated.. yet ;)

import argparse
import logging
import sys
from datetime import datetime
import os
import serial.tools.list_ports

from gcal import fetch_events
import serial_comms

def main():
    args = parse_args()
    setup_logging(args.debug)
    log = logging.getLogger(__name__)

    if args.debug:
        debug_info(args)
        return

    try:
        serial_comms.open(args.port, args.baud)
    except Exception as e:
        log.warning(f"Could not open serial port: {e}")
        log.warning("Running without Arduino connection — serial commands will be unavailable")

    while True:
        try:
            cmd = input("tengwar> ").strip()

            if not cmd:
                continue

            cmd_lower = cmd.lower()

            if cmd_lower == "next-cal":
                next_cal(args.month, args.year)
            elif cmd_lower == "sync-cal":
                sync_cal_events()
            elif cmd_lower in ("quit", "exit"):
                log.info("Shutting down")
                break
            elif cmd.upper().startswith("G") or cmd.upper().startswith("M"):
                if serial_comms._ser:
                    response = serial_comms.send_command(cmd)
                    if response:
                        log.info(f"Arduino: {response}")
                    else:
                        log.info("Arduino: (no response)")
                else:
                    log.warning("No Arduino connected — cannot send G-code")
            else:
                log.warning(f"Unknown command: '{cmd}'")

        except KeyboardInterrupt:
            log.info("Interrupted, shutting down")
            break
    
    serial_comms.close()

"""
next_cal()
Fetches and draws the next calendar. Called to set up the next calendar.
Ex: if current calendar is February then user triggers next_cal() to set up March cal.
"""
def next_cal(month: int, year: int):
    log = logging.getLogger(__name__)

    # Increment month, wrap year if needed
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    log.info(f"Drawing calendar for {next_month}/{next_year}")
    draw_cal_template(next_month, next_year)

"""
draw_cal_template()
Draws a 6 x 7 matrix for the given month (and year).
Determines the starting weekday and fills in day numbers across the grid.
Each cell maps to a plotter coordinate where origin is top-left.
"""
def draw_cal_template(month: int, year: int):
    log = logging.getLogger(__name__)

    first_day = datetime(year, month, 1)
    start_weekday = first_day.weekday()  # Monday=0, Sunday=6
    # Shift so Sunday=0 (standard calendar layout)
    start_col = (start_weekday + 1) % 7

    # How many days in this month
    if month == 12:
        days_in_month = (datetime(year + 1, 1, 1) - first_day).days
    else:
        days_in_month = (datetime(year, month + 1, 1) - first_day).days

    log.info(f"Drawing {month}/{year}: {days_in_month} days, starting col {start_col}")

    # Build 6x7 grid (rows x cols), None = empty cell
    grid = [[None] * 7 for _ in range(6)]
    day = 1
    for row in range(6):
        for col in range(7):
            cell_index = row * 7 + col
            if cell_index >= start_col and day <= days_in_month:
                grid[row][col] = day
                day += 1

    # TODO: translate grid cells to plotter G-code coordinates (draw commands sent to Arduino)
    # For now, logging the grid layout for debugging
    log.debug("Calendar grid layout:")
    days_header = " Su  Mo  Tu  We  Th  Fr  Sa"
    log.debug(days_header)
    for row in grid:
        row_str = "".join(f"{d:3}  " if d else "     " for d in row)
        log.debug(row_str)

"""
sync_cal_events()
Fetches and applies events from current calendar (additions, deletions, edits). 
Manually triggered from the terminal (for now)
"""
def sync_cal_events():
    log = logging.getLogger(__name__)
    log.info("Syncing calendar events from Google Calendar")

    events = fetch_events(datetime.now().month, datetime.now().year)        

    for event in events:
        log.info(f"  {event['start']}: {event['summary']}")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tengwar"
    )
    parser.add_argument(
        "--next-cal",
        action="store_true",
        help="Draw the next calendar"
    )
    parser.add_argument(
        "--sync-cal",
        action="store_true",
        help="Update the calendar with the latest (if any) changes"
    )
    parser.add_argument(
    "--port",
    type=str,
    default=os.getenv("DEFAULT_PORT", "/dev/ttyACM0"),
    help="Serial port the Arduino Mega is connected to (e.g. /dev/ttyACM0). Ex: python3 main.py --port /dev/ttyUSB0"
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=250000,
        help="Baud rate for serial communication (default: 250000 for RAMPS/Marlin). Ex: python3 main.py --port /dev/ttyACM0 --baud 115200"
    )
    parser.add_argument(
        "--month",
        type=int,
        default=datetime.now().month,
        help="Current month as an integer (e.g. 3 for March). Defaults to system month."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Current year (e.g. 2026). Defaults to system year."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print system info, list serial ports, and test the configured port"
    )

    return parser.parse_args()

"""
setup_logging(debug: bool)
Called once at startup. Creates two log handlers: one that prints to your terminal (useful over SSH) 
and one that writes to 'tengwar.log' on disk. If '--debug' is passed, the log level is set to DEBUG. 
"""
def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/tengwar.log"),
    ]
    logging.basicConfig(level=level, format=fmt, handlers=handlers)

"""
debug_info(args)
Prints:
    Current working directory
    Configured --port and --baud values
    Any serial port currently visible on the Pi from 'serial.tools.list_ports'
        (and whether it can actually open and connect to your configured port)
"""
def debug_info(args):
    log = logging.getLogger(__name__)
    log.debug("── Debug Info ───────────────────────────────")
    log.debug(f"Working dir    : {os.getcwd()}")
    log.debug(f"Serial port    : {args.port}")
    log.debug(f"Baud rate      : {args.baud}")
    # TODO add more info as needed

    # List all available serial ports
    ports = list(serial.tools.list_ports.comports())
    if ports:
        log.debug("Available serial ports:")
        for p in ports:
            log.debug(f"  {p.device} — {p.description}")
    else:
        log.debug("No serial ports detected")

    # Try opening the configured port
    try:
        ser = serial.Serial(args.port, args.baud, timeout=2)
        log.debug(f"Successfully opened {args.port} at {args.baud} baud")
        ser.close()
    except Exception as e:
        log.debug(f"Could not open {args.port}: {e}")

    log.debug("─────────────────────────────────────────────")

if __name__ == "__main__":
    main()