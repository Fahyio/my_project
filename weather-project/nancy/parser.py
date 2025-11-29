import argparse


def setup_parsers():
    """Настройка парсеров аргументов"""
    parser = argparse.ArgumentParser(
        description='Консольное приложение для получения погоды',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py get Москва
  python main.py get "Санкт-Петербург" --days 3
  python main.py get Лондон --no-cache
  python main.py clear-cache
  python main.py history
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Парсер для команды погоды
    weather_parser = subparsers.add_parser('get', help='Получить погоду для города')
    weather_parser.add_argument('city', help='Название города')
    weather_parser.add_argument('--days', type=int, default=1,
                                choices=range(1, 8), metavar='[1-7]',
                                help='Количество дней прогноза (по умолчанию: 1)')
    weather_parser.add_argument('--no-cache', action='store_true',
                                help='Не использовать кэш')

    # Парсер для очистки кэша
    subparsers.add_parser('clear-cache', help='Очистить кэш запросов')

    # Парсер для истории запросов
    subparsers.add_parser('history', help='Показать историю запросов')

    return parser