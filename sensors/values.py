from .sensor_input import SensorReader
from config import load_config

config = load_config()

class AirQualityAnalyzer(SensorReader):
    def analyze_source(self, pm25, pm10):
        ratio = pm25 / pm10
        if ratio >= config["thresholds"]["ratio_combustion"]:
            return "Combustion", ratio
        elif ratio <= config["thresholds"]["ratio_dust"]:
            return "Dust", ratio
        else:
            return 'Mixed', ratio

    def get_reading(self):
        pm25, pm10 = self.read_pm_values()
        source, ratio = self.analyze_source(pm25, pm10)
        
        # Update running averages
        self.pm25_readings.append(pm25)
        self.pm10_readings.append(pm10)
        
        return {
            'pm25': pm25,
            'pm10': pm10,
            'source': source,
            'ratio': ratio,
            'pm25_1hr_avg': self._calculate_avg(self.pm25_readings),
            'pm10_1hr_avg': self._calculate_avg(self.pm10_readings)
        }

    def _calculate_avg(self, readings):
        return sum(readings) / len(readings) if readings else None