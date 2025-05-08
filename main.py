from sensors.values import AirQualityAnalyzer
from AQI_Stuff import AQI_Calculator
import time

def main():
    sensor = AirQualityAnalyzer()
    aqi_calc = AQI_Calculator()
    
    try:
        while True:
            data = sensor.get_reading()
            aqi, category = aqi_calc.calculate_aqi(data['pm25'], data['pm10'])
            
            print(f"""
            Live Readings:
            PM2.5: {data['pm25']:.1f} μg/m³ | PM10: {data['pm10']:.1f} μg/m³
            Source: {data['source']} (Ratio: {data['ratio']:.2f})
            Current AQI: {aqi} ({category})
            """)
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        sensor.ser.close()
        print("Monitoring stopped")

if __name__ == "__main__":
    main()