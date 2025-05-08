import serial
from collections import deque
from config import load_config

config = load_config()

class SensorReader:
    def __init__(self, port='COM3'):
        self.ser = serial.Serial(port, baudrate=9600, timeout=2)
        self.pm25_readings = deque(maxlen=60)
        self.pm10_readings = deque(maxlen=60)

    def _read_frame(self):
        """Raw frame reading (10 bytes)"""
        while True:
            if self.ser.read(1) == b'\xaa':
                data = self.ser.read(9)
                if data[0] == 0xC0 and data[-1] == 0xAB:
                    return data

    def read_pm_values(self):
        """Extract PM2.5 and PM10 from sensor frame"""
        data = self._read_frame()
        pm25 = (data[2] * 256 + data[1]) / 10.0
        pm10 = (data[4] * 256 + data[3]) / 10.0
        return pm25, pm10