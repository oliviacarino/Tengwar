# serial_comms.py

import serial
import logging
import time

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
def send_command(cmd: str):
    if not _ser or not _ser.is_open:
        log.warning("Serial port not open")
        return
    _ser.write((cmd.strip() + "\n").encode())
    log.debug(f"Sent: {cmd}")

"""
read_response(timeout: float) -> str
Reads lines from the Arduino until 'ok' is received or timeout.
Returns the full response as a string.
"""
def read_response(timeout: float = 2.0) -> str:
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