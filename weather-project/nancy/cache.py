import json
import os
from datetime import datetime, timedelta
import hashlib


class WeatherCache:
    def __init__(self, cache_file='weather_cache.json', ttl_hours=1):
        self.cache_file = cache_file
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_cache_file()

    def _ensure_cache_file(self):
        """Создает файл кэша если он не существует"""
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _get_cache_key(self, city_name, days):
        """Создает ключ для кэша на основе города и количества дней"""
        key_string = f"{city_name.lower()}_{days}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, city_name, days):
        """Получение данных из кэша"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            cache_key = self._get_cache_key(city_name, days)
            cached_data = cache.get(cache_key)

            if cached_data:
                cached_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - cached_time < self.ttl:
                    return cached_data['data']

            return None
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def set(self, city_name, days, data):
        """Сохранение данных в кэш"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            cache = {}

        cache_key = self._get_cache_key(city_name, days)
        cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'city': city_name,
            'days': days
        }

        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def clear(self):
        """Очистка кэша"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        self._ensure_cache_file()

    def get_history(self):
        """Получение истории запросов"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            history = []
            for key, data in cache.items():
                history.append({
                    'city': data.get('city', 'Unknown'),
                    'days': data.get('days', 1),
                    'timestamp': data.get('timestamp', 'Unknown')
                })

            return sorted(history, key=lambda x: x['timestamp'], reverse=True)
        except (json.JSONDecodeError, FileNotFoundError):
            return []