import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import gcode

class TestBasicMoves(unittest.TestCase):

    def test_home(self):
        self.assertEqual(gcode.home(), "G28 X Y")

    def test_move(self):
        self.assertEqual(gcode.move(10, 20), "G1 X10.000 Y20.000 F3000")

    def test_move_custom_feedrate(self):
        self.assertEqual(gcode.move(10, 20, feedrate=1500), "G1 X10.000 Y20.000 F1500")

    def test_move_rapid(self):
        self.assertEqual(gcode.move_rapid(10, 20), "G0 X10.000 Y20.000 F6000")

    def test_move_rapid_custom_feedrate(self):
        self.assertEqual(gcode.move_rapid(10, 20, feedrate=3000), "G0 X10.000 Y20.000 F3000")


class TestPenControl(unittest.TestCase):

    def test_pen_up(self):
        self.assertEqual(gcode.pen_up(), f"M280 P0 S{gcode.PEN_UP_ANGLE}")

    def test_pen_down(self):
        self.assertEqual(gcode.pen_down(), f"M280 P0 S{gcode.PEN_DOWN_ANGLE}")

    def test_disable_motors(self):
        self.assertEqual(gcode.disable_motors(), "M18")


class TestCalibration(unittest.TestCase):

    def test_set_steps_per_mm(self):
        self.assertEqual(gcode.set_steps_per_mm(80, 80), "M92 X80.000 Y80.000")

    def test_save_settings(self):
        self.assertEqual(gcode.save_settings(), "M500")


class TestDrawLine(unittest.TestCase):

    def test_returns_list(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertIsInstance(result, list)

    def test_correct_length(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertEqual(len(result), 5)

    def test_starts_with_pen_up(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertEqual(result[0], gcode.pen_up())

    def test_ends_with_pen_up(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertEqual(result[-1], gcode.pen_up())

    def test_pen_down_before_draw(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertEqual(result[2], gcode.pen_down())

    def test_rapid_move_to_start(self):
        result = gcode.draw_line(5, 5, 10, 10)
        self.assertEqual(result[1], gcode.move_rapid(5, 5))

    def test_draw_to_end(self):
        result = gcode.draw_line(0, 0, 10, 10)
        self.assertEqual(result[3], gcode.move(10, 10))


class TestDrawRectangle(unittest.TestCase):

    def test_returns_list(self):
        result = gcode.draw_rectangle(0, 0, 50, 50)
        self.assertIsInstance(result, list)

    def test_starts_with_pen_up(self):
        result = gcode.draw_rectangle(0, 0, 50, 50)
        self.assertEqual(result[0], gcode.pen_up())

    def test_ends_with_pen_up(self):
        result = gcode.draw_rectangle(0, 0, 50, 50)
        self.assertEqual(result[-1], gcode.pen_up())

    def test_moves_to_top_left(self):
        result = gcode.draw_rectangle(10, 20, 50, 50)
        self.assertEqual(result[1], gcode.move_rapid(10, 20))

    def test_draws_four_sides(self):
        # pen_up, move_rapid, pen_down, 4 sides, pen_up = 8 commands
        result = gcode.draw_rectangle(0, 0, 50, 50)
        self.assertEqual(len(result), 8)


class TestDrawDayNumber(unittest.TestCase):

    def test_returns_list(self):
        result = gcode.draw_day_number(1, 0, 0, 76.2, 76.2)
        self.assertIsInstance(result, list)

    def test_not_empty(self):
        result = gcode.draw_day_number(15, 0, 0, 76.2, 76.2)
        self.assertGreater(len(result), 0)

    def test_starts_with_pen_up(self):
        result = gcode.draw_day_number(1, 0, 0, 76.2, 76.2)
        self.assertEqual(result[0], gcode.pen_up())

    def test_ends_with_pen_up(self):
        result = gcode.draw_day_number(1, 0, 0, 76.2, 76.2)
        self.assertEqual(result[-1], gcode.pen_up())

    def test_single_digit_day(self):
        result = gcode.draw_day_number(5, 0, 0, 76.2, 76.2)
        self.assertIsInstance(result, list)

    def test_double_digit_day(self):
        result = gcode.draw_day_number(31, 0, 0, 76.2, 76.2)
        self.assertIsInstance(result, list)


class TestDrawMonthName(unittest.TestCase):

    def test_returns_list(self):
        result = gcode.draw_month_name(1, 0, 0, 533.4)
        self.assertIsInstance(result, list)

    def test_not_empty(self):
        result = gcode.draw_month_name(4, 0, 0, 533.4)
        self.assertGreater(len(result), 0)

    def test_starts_with_pen_up(self):
        result = gcode.draw_month_name(1, 0, 0, 533.4)
        self.assertEqual(result[0], gcode.pen_up())

    def test_ends_with_pen_up(self):
        result = gcode.draw_month_name(1, 0, 0, 533.4)
        self.assertEqual(result[-1], gcode.pen_up())

    def test_all_months(self):
        # Make sure none of the 12 months throw an error
        for month in range(1, 13):
            result = gcode.draw_month_name(month, 0, 0, 533.4)
            self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()