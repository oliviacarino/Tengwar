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
Fetches and draws the next calendar. 
Ex: if current calendar is February then next_cal() will March, etc.
"""
def next_cal():

"""
draw_cal_template():
Draws a 6 x 7 grid.
"""
# def draw_cal_template():

# def sync_cal_events()

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

    return parser.parse_args()

if __name__ == "__main__":
    main()