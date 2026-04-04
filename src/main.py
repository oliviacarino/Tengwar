# Initialize 
# Via CLI -- draw next calendar, manually trigger calendar sync 
# Trigger calendar sync every 4 hours (pull new events, deletions, edits)

# Actions
# Process calendar template, publish to printer
# Process calendar event data, publish to printer

import argparse

def main():
    args = parse_args()

    if args.next_cal:
        next_cal()
        return
    if args.sync_cal:
        sync_cal_events()

"""
next_cal()
Fetches and draws the next calendar. Called to set up the next calendar.
Ex: if current calendar is February then user triggers next_cal() to set up March cal.
"""
def next_cal():
    pass

"""
draw_cal_template()
Draws a 6 x 7 grid.
"""
def draw_cal_template():
    pass

"""
sync_cal_events()
Fetches and applies events from current calendar. 
"""
def sync_cal_events():
    pass

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
    default="/dev/ttyACM0",
    help="Serial port the Arduino Mega is connected to (e.g. /dev/ttyACM0). Ex: python3 main.py --port /dev/ttyUSB0"
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=250000,
        help="Baud rate for serial communication (default: 250000 for RAMPS/Marlin). Ex: python3 main.py --port /dev/ttyACM0 --baud 115200"
    )

    return parser.parse_args()

if __name__ == "__main__":
    main()