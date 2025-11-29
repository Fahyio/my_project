import requests
import json
from datetime import datetime, timedelta


class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_city_coordinates(self, city_name):
        """Получение координат города через Geocoding API"""
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            'name': city_name,
            'count': 1,
            'language': 'ru',
            'format': 'json'
        }

        try:
            response = requests.get(geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('results'):
                raise ValueError(f"Город '{city_name}' не найден")

            city_data = data['results'][0]
            return {
                'latitude': city_data['latitude'],
                'longitude': city_data['longitude'],
                'name': city_data['name'],
                'country': city_data.get('country', 'N/A')
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при получении координат: {e}")

    def get_weather_forecast(self, latitude, longitude, days=1):
        """Получение прогноза погоды"""
        if days < 1 or days > 7:
            raise ValueError("Количество дней должно быть от 1 до 7")

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum', 'weather_code'],
            'timezone': 'auto',
            'forecast_days': days
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при получении погоды: {e}")

    def get_weather_data(self, city_name, days=1):
        """Основной метод для получения данных о погоде"""
        # Получаем координаты города
        coordinates = self.get_city_coordinates(city_name)

        # Получаем прогноз погоды
        weather_data = self.get_weather_forecast(
            coordinates['latitude'],
            coordinates['longitude'],
            days
        )

        return {
            'city_info': coordinates,
            'weather_data': weather_data,
            'timestamp': datetime.now().isoformat()
        }


class WeatherDecoder:
    """Класс для декодирования погодных кодов"""

    @staticmethod
    def get_weather_description(weather_code):
        """Преобразование кода погоды в текстовое описание"""
        weather_codes = {
            0: 'Ясно',
            1: 'Преимущественно ясно',
            2: 'Переменная облачность',
            3: 'Пасмурно',
            45: 'Туман',
            48: 'Туман с инеем',
            51: 'Морось: слабая',
            53: 'Морось: умеренная',
            55: 'Морось: сильная',
            61: 'Дождь: слабый',
            63: 'Дождь: умеренный',
            65: 'Дождь: сильный',
            80: 'Ливень: слабый',
            81: 'Ливень: умеренный',
            82: 'Ливень: сильный',
            95: 'Гроза',
            96: 'Гроза со слабым градом',
            99: 'Гроза с сильным градом'
        }
        return weather_codes.get(weather_code, 'Неизвестно')