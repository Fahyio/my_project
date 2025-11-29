from .api import WeatherAPI, WeatherDecoder
from .cache import WeatherCache
from datetime import datetime

# Инициализация компонентов
api = WeatherAPI()
cache = WeatherCache()
decoder = WeatherDecoder()


def get_weather(city_name, days=1, use_cache=True):
    """Основная команда для получения погоды"""
    # Проверяем кэш если нужно
    if use_cache:
        cached_data = cache.get(city_name, days)
        if cached_data:
            print("📁 Данные загружены из кэша")
            display_weather_data(cached_data)
            return

    # Получаем свежие данные
    print("🌐 Загрузка данных с API...")
    try:
        weather_data = api.get_weather_data(city_name, days)

        # Сохраняем в кэш
        cache.set(city_name, days, weather_data)

        display_weather_data(weather_data)

    except Exception as e:
        raise Exception(f"Не удалось получить данные о погоде: {e}")


def display_weather_data(data):
    """Отображение данных о погоде в консоли"""
    city_info = data['city_info']
    weather_data = data['weather_data']

    print(f"\n📍 {city_info['name']}, {city_info['country']}")
    print(f"📅 Прогноз погоды на {len(weather_data['daily']['time'])} дней")
    print("=" * 50)

    daily_data = weather_data['daily']

    for i in range(len(daily_data['time'])):
        date = daily_data['time'][i]
        temp_max = daily_data['temperature_2m_max'][i]
        temp_min = daily_data['temperature_2m_min'][i]
        precipitation = daily_data['precipitation_sum'][i]
        weather_code = daily_data['weather_code'][i]

        # Форматируем дату
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d.%m.%Y')

        # Получаем описание погоды
        weather_desc = decoder.get_weather_description(weather_code)

        print(f"\n📅 {formatted_date}:")
        print(f"   🌡  Температура: {temp_min:.1f}°C - {temp_max:.1f}°C")
        print(f"   ☁️  Погода: {weather_desc}")
        print(f"   💧 Осадки: {precipitation} mm")

    print("\n" + "=" * 50)
    print(f"🕐 Данные обновлены: {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}")


def clear_cache():
    """Команда для очистки кэша"""
    cache.clear()
    print("✅ Кэш успешно очищен")


def show_history():
    """Команда для показа истории запросов"""
    history = cache.get_history()

    if not history:
        print("📝 История запросов пуста")
        return

    print("📝 История запросов:")
    print("=" * 60)

    for i, item in enumerate(history[:10], 1):  # Показываем последние 10 запросов
        try:
            timestamp = datetime.fromisoformat(item['timestamp'])
            formatted_time = timestamp.strftime('%d.%m.%Y %H:%M')
            print(f"{i:2d}. {item['city']:15} | {item['days']} дн. | {formatted_time}")
        except (ValueError, KeyError):
            continue

    if len(history) > 10:
        print(f"\n... и еще {len(history) - 10} запросов")