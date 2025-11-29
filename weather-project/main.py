#!/usr/bin/env python3
import argparse
import sys
import os

# Добавляем путь к пакету
sys.path.append(os.path.join(os.path.dirname(__file__), 'nancy'))

from nancy.commands import get_weather, clear_cache, show_history


def main():
    parser = argparse.ArgumentParser(description='Консольное приложение для получения погоды')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Парсер для команды погоды
    weather_parser = subparsers.add_parser('get', help='Получить погоду для города')
    weather_parser.add_argument('city', help='Название города')
    weather_parser.add_argument('--days', type=int, default=1, help='Количество дней прогноза (1-7)')
    weather_parser.add_argument('--no-cache', action='store_true', help='Не использовать кэш')

    # Парсер для очистки кэша
    subparsers.add_parser('clear-cache', help='Очистить кэш')

    # Парсер для истории запросов
    subparsers.add_parser('history', help='Показать историю запросов')

    args = parser.parse_args()

    try:
        if args.command == 'get':
            get_weather(args.city, args.days, not args.no_cache)
        elif args.command == 'clear-cache':
            clear_cache()
        elif args.command == 'history':
            show_history()
        else:
            parser.print_help()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()