import unittest
import sys
import os
from unittest.mock import MagicMock, patch, call

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import serial_comms

class TestOpen(unittest.TestCase):

    @patch('serial_comms.serial.Serial')
    def test_opens_correct_port(self, mock_serial):
        serial_comms.open('/dev/ttyACM0', 250000)
        mock_serial.assert_called_once_with('/dev/ttyACM0', 250000, timeout=2)

    @patch('serial_comms.serial.Serial')
    def test_returns_serial_object(self, mock_serial):
        result = serial_comms.open('/dev/ttyACM0', 250000)
        self.assertIsNotNone(result)

    @patch('serial_comms.serial.Serial')
    def test_sets_global_ser(self, mock_serial):
        serial_comms.open('/dev/ttyACM0', 250000)
        self.assertIsNotNone(serial_comms._ser)

    @patch('serial_comms.serial.Serial')
    def test_raises_on_bad_port(self, mock_serial):
        mock_serial.side_effect = serial_comms.serial.SerialException("port not found")
        with self.assertRaises(serial_comms.serial.SerialException):
            serial_comms.open('/dev/bad_port', 250000)


class TestSendCommand(unittest.TestCase):

    def setUp(self):
        serial_comms._ser = MagicMock()
        serial_comms._ser.is_open = True
        serial_comms._ser.in_waiting = 0

    def tearDown(self):
        serial_comms._ser = None

    def test_sends_command_with_newline(self):
        with patch.object(serial_comms, 'read_response', return_value="ok"):
            serial_comms.send_command('M115')
            serial_comms._ser.write.assert_called_once_with(b'M115\n')

    def test_strips_whitespace_before_sending(self):
        with patch.object(serial_comms, 'read_response', return_value="ok"):
            serial_comms.send_command('  M115  ')
            serial_comms._ser.write.assert_called_once_with(b'M115\n')

    def test_resets_input_buffer_before_send(self):
        serial_comms.send_command('M115')
        serial_comms._ser.reset_input_buffer.assert_called()

    def test_flushes_after_write(self):
        serial_comms.send_command('M115')
        serial_comms._ser.flush.assert_called()

    def test_returns_empty_string_when_no_ser(self):
        serial_comms._ser = None
        result = serial_comms.send_command('M115')
        self.assertEqual(result, "")

    def test_returns_empty_string_when_port_closed(self):
        serial_comms._ser.is_open = False
        result = serial_comms.send_command('M115')
        self.assertEqual(result, "")

    def test_retries_on_no_response(self):
        # read_response will return "" each time, triggering retries
        with patch.object(serial_comms, 'read_response', return_value=""):
            serial_comms.send_command('M115', retries=3)
            self.assertEqual(serial_comms._ser.write.call_count, 3)

    def test_returns_response_on_success(self):
        with patch.object(serial_comms, 'read_response', return_value="ok"):
            result = serial_comms.send_command('M115')
            self.assertEqual(result, "ok")

    def test_stops_retrying_after_success(self):
        with patch.object(serial_comms, 'read_response', return_value="ok"):
            serial_comms.send_command('M115', retries=3)
            # Should only write once since first attempt succeeds
            self.assertEqual(serial_comms._ser.write.call_count, 1)


class TestReadResponse(unittest.TestCase):

    def setUp(self):
        serial_comms._ser = MagicMock()
        serial_comms._ser.is_open = True

    def tearDown(self):
        serial_comms._ser = None

    def test_returns_empty_when_no_ser(self):
        serial_comms._ser = None
        result = serial_comms.read_response()
        self.assertEqual(result, "")

    def test_returns_empty_when_port_closed(self):
        serial_comms._ser.is_open = False
        result = serial_comms.read_response()
        self.assertEqual(result, "")

    def test_reads_until_ok(self):
        responses = [b'Marlin 2.1\n', b'ok\n']
        serial_comms._ser.in_waiting = 1
        serial_comms._ser.readline.side_effect = responses
        result = serial_comms.read_response()
        self.assertIn("ok", result)

    def test_returns_multiline_response(self):
        responses = [b'line one\n', b'line two\n', b'ok\n']
        serial_comms._ser.in_waiting = 1
        serial_comms._ser.readline.side_effect = responses
        result = serial_comms.read_response()
        self.assertIn("line one", result)
        self.assertIn("line two", result)

    def test_joins_lines_with_newline(self):
        responses = [b'hello\n', b'ok\n']
        serial_comms._ser.in_waiting = 1
        serial_comms._ser.readline.side_effect = responses
        result = serial_comms.read_response()
        self.assertEqual(result, "hello\nok")


class TestClose(unittest.TestCase):

    def test_closes_open_connection(self):
        mock_ser = MagicMock()
        mock_ser.is_open = True
        serial_comms._ser = mock_ser
        serial_comms.close()
        mock_ser.close.assert_called_once()

    def test_sets_ser_to_none(self):
        serial_comms._ser = MagicMock()
        serial_comms._ser.is_open = True
        serial_comms.close()
        self.assertIsNone(serial_comms._ser)

    def test_does_not_crash_when_already_none(self):
        serial_comms._ser = None
        try:
            serial_comms.close()
        except Exception as e:
            self.fail(f"close() raised an exception with _ser=None: {e}")

    def test_does_not_close_when_already_closed(self):
        mock_ser = MagicMock()
        mock_ser.is_open = False
        serial_comms._ser = mock_ser
        serial_comms.close()
        mock_ser.close.assert_not_called()


if __name__ == "__main__":
    unittest.main()