import serial
import time
from collections import deque

'''
AQI Calculator Module for SDS011 Sensor
- Calculates 1-hour average AQI from PM2.5/PM10
- Uses EPA/WHO breakpoints
'''

# AQI Breakpoints (1-hour averages)
AQI_BREAKPOINTS_PM25_1HR = [
    (0, 12.0, 0, 50),       # Good
    (12.1, 35.4, 51, 100),  # Moderate
    (35.5, 55.4, 101, 150), # Unhealthy for Sensitive Groups
    (55.5, 150.4, 151, 200), # Unhealthy
    (150.5, 250.4, 201, 300), # Very Unhealthy
    (250.5, 500.4, 301, 500)  # Hazardous
]

AQI_BREAKPOINTS_PM10_1HR = [
    (0, 54, 0, 50),         # Good
    (55, 154, 51, 100),     # Moderate
    (155, 254, 101, 150),   # USG
    (255, 354, 151, 200),   # Unhealthy
    (355, 424, 201, 300),   # Very Unhealthy
    (425, 604, 301, 500)    # Hazardous
]

class AQI_Calculator:
    def __init__(self):
        self.pm25_readings = deque(maxlen=60)
        self.pm10_readings = deque(maxlen=60)
    
    def add_reading(self, pm25, pm10):
        """Add new sensor readings"""
        self.pm25_readings.append(pm25)
        self.pm10_readings.append(pm10)
    
    def get_1hr_avg(self):
        """Calculate 1-hour averages"""
        if len(self.pm25_readings) == 0:
            return None, None
        return (
            sum(self.pm25_readings) / len(self.pm25_readings),
            sum(self.pm10_readings) / len(self.pm10_readings)
        )
    
    def calculate_aqi(self, pm25=None, pm10=None):
        """
        Calculate current AQI
        Args:
            pm25/pm10: Optional immediate readings (bypasses averaging)
        Returns:
            AQI value (0-500), category string
        """
        if pm25 is None or pm10 is None:
            pm25_avg, pm10_avg = self.get_1hr_avg()
            if pm25_avg is None:
                return None, "No data"
        else:
            pm25_avg, pm10_avg = pm25, pm10
        
        def _compute_aqi(Cp, breakpoints):
            for (Clo, Chi, Ilo, Ihi) in breakpoints:
                if Clo <= Cp <= Chi:
                    return ((Ihi - Ilo)/(Chi - Clo)) * (Cp - Clo) + Ilo
            return 500
        
        aqi_pm25 = _compute_aqi(pm25_avg, AQI_BREAKPOINTS_PM25_1HR)
        aqi_pm10 = _compute_aqi(pm10_avg, AQI_BREAKPOINTS_PM10_1HR)
        aqi = max(aqi_pm25, aqi_pm10)
        
        categories = [
            (0, 50, "Good"),
            (51, 100, "Moderate"),
            (101, 150, "Unhealthy for Sensitive Groups"),
            (151, 200, "Unhealthy"),
            (201, 300, "Very Unhealthy"),
            (301, 500, "Hazardous")
        ]
        
        for lo, hi, category in categories:
            if lo <= aqi <= hi:
                return round(aqi), category
        return 500, "Hazardous"