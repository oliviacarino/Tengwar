# serial_comms.py

import serial
import logging
import time

MAX_RETRIES = 3
RETRY_DELAY = 0.5
RESPONSE_TIMEOUT = 30.0

log = logging.getLogger(__name__)

_ser = None

"""
open(port: str, baud: int, timeout: int)
Opens a serial connection to the Arduino.
"""
def open(port: str, baud: int, timeout: int = 2):
    global _ser
    _ser = serial.Serial(port, baud, timeout=timeout)
    log.info(f"Connected to Arduino on {port} at {baud} baud")
    time.sleep(2)  # Give Marlin time to boot
    return _ser

"""
send_command(cmd: str)
Sends a G-code command to the Arduino.
"""
def send_command(cmd: str, retries: int = MAX_RETRIES):
    if not _ser or not _ser.is_open:
        log.warning("Serial port not open")
        return ""
    
    for attempt in range(1, retries + 1):
        try:
            _ser.reset_input_buffer()
            _ser.write((cmd.strip() + "\n").encode())
            _ser.flush()
            time.sleep(0.1)
            log.debug(f"Sent (attempt {attempt}/{retries}): {cmd}")

            response = read_response()
            if response:
                return response

            log.warning(f"No response on attempt {attempt}/{retries} for command: {cmd}")
            time.sleep(RETRY_DELAY)

        except serial.SerialException as e:
            log.warning(f"Serial error on attempt {attempt}/{retries}: {e}")
            time.sleep(RETRY_DELAY)

    log.error(f"No response after {retries} attempts for command: {cmd}")
    return ""

"""
read_response(timeout: float) -> str
Reads lines from the Arduino until 'ok' is received or timeout.
Returns the full response as a string.
"""
def read_response(timeout: float = RESPONSE_TIMEOUT) -> str:
    if not _ser or not _ser.is_open:
        return ""
    response = []
    start = time.time()
    while time.time() - start < timeout:
        if _ser.in_waiting:
            line = _ser.readline().decode(errors="replace").strip()
            if line:
                response.append(line)
            if line == "ok":
                break
        else:
            time.sleep(0.01)

    if not response:
        log.debug(f"read_response timed out after {timeout}s")

    return "\n".join(response)

"""
close()
Closes the serial connection.
"""
def close():
    global _ser
    if _ser and _ser.is_open:
        _ser.close()
        log.info("Serial connection closed")
    _ser = None