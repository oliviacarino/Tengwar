# Generates G-code command strings for the Tengwar XY plotter.
# Functions return strings only — use serial_comms.send_command() to execute them.
#
# Axis orientation:
#   X = horizontal
#   Y = vertical
#   Origin (0, 0) = top-left of plotter area
#
# Pen up/down control via servo on RAMPS servo header (servo index 0)

from HersheyFonts import HersheyFonts

# Servo angles (TODO correctly tune once shield/parts are added)
PEN_UP_ANGLE = 90    # degrees — pen lifted off paper
PEN_DOWN_ANGLE = 45  # degrees — pen touching paper
SERVO_INDEX = 0

# Text padding inside calendar cells (mm)
CELL_PADDING = 3.0

# Font setup
_day_font = HersheyFonts()
_day_font.load_default_font('rowmand')

_month_font = HersheyFonts()
_month_font.load_default_font('gothiceng')

"""
home() -> str
Homes both X and Y axes.
Sends the plotter to the origin (0, 0) via limit switches.
"""
def home() -> str:
    return "G28 X Y"

"""
move(x: float, y: float, feedrate: int) -> str
Moves the pen to an absolute XY position at the given feedrate (mm/min).
Pen state is not changed — call pen_up() or pen_down() separately.
"""
def move(x: float, y: float, feedrate: int = 3000) -> str:
    return f"G1 X{x:.3f} Y{y:.3f} F{feedrate}"

"""
move_rapid(x: float, y: float, feedrate: int) -> str
Rapid move to an absolute XY position (no drawing).
Use for repositioning without drawing a line.
Higher default feedrate than move() since no precision needed.
"""
def move_rapid(x: float, y: float, feedrate: int = 6000) -> str:
    return f"G0 X{x:.3f} Y{y:.3f} F{feedrate}"

"""
pen_up() ->  str
Lifts the pen off the paper via servo.
Call before any rapid move to avoid unwanted marks.
"""
def pen_up() -> str:
    return f"M280 P{SERVO_INDEX} S{PEN_UP_ANGLE}"

"""
pen_down() -> str
Lowers the pen onto the paper via servo.
Call before any drawing move.
"""
def pen_down() -> str:
    return f"M280 P{SERVO_INDEX} S{PEN_DOWN_ANGLE}"

"""
disable_motors() -> str
Disables all stepper motors.
Call after drawing is complete to reduce heat and power draw.
Note: position will be lost after calling this.
"""
def disable_motors() -> str:
    return "M18"

"""
set_steps_per_mm(x: float, y: float) -> str
Sets steps per mm for X and Y axes.
Use during calibration. Save to EEPROM with save_settings().
"""
def set_steps_per_mm(x: float, y: float) -> str:
    return f"M92 X{x:.3f} Y{y:.3f}"

"""
save_settings() -> str 
Saves current settings (steps/mm, etc.) to EEPROM.
Call after set_steps_per_mm() to persist across reboots.
"""
def save_settings() -> str:
    return "M500"

"""
draw_line(x1: float, y1: float, x2: float, y2: float, feedrate: int) -> list
Draws a straight line from (x1, y1) to (x2, y2).
Returns a list of G-code strings in order of execution:
    1. Lift pen
    2. Rapid move to start
    3. Lower pen
    4. Draw to end
    5. Lift pen
"""
def draw_line(x1: float, y1: float, x2: float, y2: float, feedrate: int = 3000) -> list:
    return [
        pen_up(),
        move_rapid(x1, y1),
        pen_down(),
        move(x2, y2, feedrate),
        pen_up(),
    ]

"""
draw_rectangle(x: float, y: float, width: float, height: float, feedrate: int) -> list
Draws a rectangle with top-left corner at (x, y).
Returns a list of G-code strings in order of execution.
"""
def draw_rectangle(x: float, y: float, width: float, height: float, feedrate: int = 3000) -> list:
    return [
        pen_up(),
        move_rapid(x, y),
        pen_down(),
        move(x + width, y, feedrate),
        move(x + width, y + height, feedrate),
        move(x, y + height, feedrate),
        move(x, y, feedrate),
        pen_up(),
    ]

"""
draw_text(text: str, x: float, y: float, size: float, font: HersheyFonts, feedrate: int) -> list
Draws a string using the given Hershey font starting at (x, y).
size controls the height of the text in mm.
Returns a list of G-code strings.

The font is normalized so that text height = size mm.
Each stroke is drawn as: pen_up → rapid to start → pen_down → draw segments → pen_up.
"""
def draw_text(text: str, x: float, y: float, size: float, font: HersheyFonts, feedrate: int = 1500) -> list:
    font.normalize_rendering(size)
    commands = [pen_up()]  # always start with pen up
    pen_is_up = True
    prev_end = None

    for (x1, y1), (x2, y2) in font.lines_for_text(text):
        px1 = x + x1
        py1 = y + y1
        px2 = x + x2
        py2 = y + y2

        if prev_end is None or (abs(px1 - prev_end[0]) > 0.01 or abs(py1 - prev_end[1]) > 0.01):
            if not pen_is_up:
                commands.append(pen_up())
                pen_is_up = True
            commands.append(move_rapid(px1, py1))

        if pen_is_up:
            commands.append(pen_down())
            pen_is_up = False

        commands.append(move(px2, py2, feedrate))
        prev_end = (px2, py2)

    if not pen_is_up:
        commands.append(pen_up())

    return commands

"""
draw_day_number(day: int, cell_x: float, cell_y: float, cell_width: float, cell_height: float, feedrate: int) -> list
Draws a day number in the top-right corner of a calendar cell.
Positioned with CELL_PADDING from the right and top borders.

Args:
    day: the day number (1-31)
    cell_x: X coordinate of the cell's top-left corner (mm)
    cell_y: Y coordinate of the cell's top-left corner (mm)
    cell_width: width of the cell (mm)
    cell_height: height of the cell (mm)
"""
def draw_day_number(day: int, cell_x: float, cell_y: float, cell_width: float, cell_height: float, feedrate: int = 1500) -> list:
    text = str(day)
    size = 8.0  # text height in mm — tune as needed

    # Estimate text width: roughly 0.6 * size per character for rowmand
    estimated_width = len(text) * size * 0.6

    # Position: top-right of cell with padding
    text_x = cell_x + cell_width - estimated_width - CELL_PADDING
    text_y = cell_y + CELL_PADDING

    return draw_text(text, text_x, text_y, size, _day_font, feedrate)

"""
draw_month_name(month: int, grid_x: float, grid_y: float, grid_width: float, feedrate: int) -> list
Draws the month name centered above the top border of the calendar grid.

Args:
    month: month as integer (1-12)
    grid_x: X coordinate of the grid's top-left corner (mm)
    grid_y: Y coordinate of the grid's top border (mm)
    grid_width: total width of the calendar grid (mm)
"""
def draw_month_name(month: int, grid_x: float, grid_y: float, grid_width: float, feedrate: int = 1500) -> list:
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    text = month_names[month - 1]
    size = 10.0  # text height in mm — tune as needed

    # Estimate text width: roughly 0.6 * size per character for gothiceng
    estimated_width = len(text) * size * 0.6

    # Center above the grid
    text_x = grid_x + (grid_width - estimated_width) / 2
    text_y = grid_y - size - CELL_PADDING  # above the top border

    return draw_text(text, text_x, text_y, size, _month_font, feedrate)