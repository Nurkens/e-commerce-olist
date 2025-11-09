"""
Custom Weather Exporter for Kazakhstan using OpenWeather API
Collects real weather metrics for multiple cities.
"""

from prometheus_client import start_http_server, Gauge, Counter
import requests
import time
import logging
import sys
import os
from dotenv import load_dotenv

# --- Load API key from .env ---
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    logging.error("❌ OPENWEATHER_API_KEY not found in .env file")
    sys.exit(1)

# --- Настройка логгирования ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- Список крупных городов Казахстана с координатами ---
cities = [
    {"name": "Astana", "lat": 51.1694, "lon": 71.4491},
    {"name": "Almaty", "lat": 43.2220, "lon": 76.8512},
    {"name": "Shymkent", "lat": 42.3417, "lon": 69.5901},
    {"name": "Karaganda", "lat": 49.8066, "lon": 73.0853},
    {"name": "Aktobe", "lat": 50.2839, "lon": 57.1668},
]

# --- Метрики ---
weather_temperature = Gauge('weather_temperature_celsius', 'Current temperature', ['city', 'country'])
weather_temperature_min = Gauge('weather_temperature_min_celsius', 'Minimum temperature', ['city', 'country'])
weather_temperature_max = Gauge('weather_temperature_max_celsius', 'Maximum temperature', ['city', 'country'])
weather_feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature', ['city', 'country']) 
weather_windspeed = Gauge('weather_windspeed_ms', 'Current wind speed in m/s', ['city', 'country'])
weather_humidity = Gauge('weather_humidity_percent', 'Current humidity', ['city', 'country'])
weather_pressure = Gauge('weather_pressure_hpa', 'Air pressure', ['city', 'country'])
weather_precipitation = Gauge('weather_precipitation_mm', 'Precipitation', ['city', 'country'])
weather_cloudcover = Gauge('weather_cloudcover_percent', 'Cloud coverage', ['city', 'country'])
weather_visibility = Gauge('weather_visibility_meters', 'Visibility distance', ['city', 'country'])
weather_api_response_time = Gauge('weather_api_response_time_seconds', 'API response time in seconds')
weather_api_calls_total = Counter('weather_api_calls_total', 'Total API calls', ['status'])
weather_city_errors = Counter('weather_city_errors_total', 'Total errors per city', ['city'])

def fetch_weather_data():
    total_calls = 0
    success_calls = 0
    
    for city in cities:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': city['lat'],
                'lon': city['lon'],
                'appid': API_KEY,
                'units': 'metric'
            }

            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            
            total_calls += 1
            weather_api_response_time.set(response_time)

            if response.status_code == 200:
                data = response.json()
                labels = {'city': city['name'], 'country': 'Kazakhstan'}

                # Основные метрики
                weather_temperature.labels(**labels).set(data['main']['temp'])
                weather_temperature_min.labels(**labels).set(data['main']['temp_min'])
                weather_temperature_max.labels(**labels).set(data['main']['temp_max'])
                weather_feels_like.labels(**labels).set(data['main']['feels_like'])
                weather_humidity.labels(**labels).set(data['main']['humidity'])
                weather_pressure.labels(**labels).set(data['main']['pressure'])
                
                # Ветер
                weather_windspeed.labels(**labels).set(data['wind']['speed'])
                
                # Облачность и видимость
                weather_cloudcover.labels(**labels).set(data['clouds']['all'])
                weather_visibility.labels(**labels).set(data.get('visibility', 0))
                
                # Осадки (может отсутствовать)
                rain_data = data.get('rain', {})
                snow_data = data.get('snow', {})
                precipitation = rain_data.get('1h', 0) or snow_data.get('1h', 0)
                weather_precipitation.labels(**labels).set(precipitation)

                success_calls += 1
                weather_api_calls_total.labels(status='success').inc()
                logging.info(f"✅ Weather data updated for {city['name']}: {data['main']['temp']}°C")
                
            else:
                weather_api_calls_total.labels(status='error').inc()
                weather_city_errors.labels(city=city['name']).inc()
                logging.error(f"❌ API error for {city['name']}: HTTP {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            weather_api_calls_total.labels(status='error').inc()
            weather_city_errors.labels(city=city['name']).inc()
            logging.error(f"❌ Request failed for {city['name']}: {e}")
        except KeyError as e:
            weather_api_calls_total.labels(status='error').inc()
            weather_city_errors.labels(city=city['name']).inc()
            logging.error(f"❌ Data parsing error for {city['name']}: Missing key {e}")
        except Exception as e:
            weather_api_calls_total.labels(status='error').inc()
            weather_city_errors.labels(city=city['name']).inc()
            logging.error(f"❌ Unexpected error for {city['name']}: {e}")

    logging.info(f"📊 API calls summary: {success_calls}/{total_calls} successful")

if __name__ == '__main__':
    start_http_server(8000)
    logging.info("🌤️ Custom Prometheus Weather Exporter started on port 8000")
    logging.info(f"📌 Monitoring {len(cities)} cities in Kazakhstan")
    logging.info("⏰ Update interval: 20 seconds")

    while True:
        try:
            fetch_weather_data()
        except KeyboardInterrupt:
            logging.info("Exporter stopped manually.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
        time.sleep(20)  # обновление каждые 20 секунд