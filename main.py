import datetime
import argparse
import pandas
import sys
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict


def format_age(years):
    if 11 <= years % 100 <= 19:
        return f"{years} лет"
    if years % 10 == 1:
        return f"{years} год"
    if 2 <= years % 10 <= 4:
        return f"{years} года"
    return f"{years} лет"


def create_parser():
    parser = argparse.ArgumentParser(
        description='Создаем сайт по шаблону'
    )
    parser.add_argument(
        "-w", "--wine",
        help="таблица вин"
    )
    return parser


def main():
    age = datetime.date.today().year - 1920
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    wine_file = (
        namespace.wine
        or os.getenv('WINE_CATALOG')
        or 'wine3.xlsx'
        )
    print(f"Использую файл: {wine_file}")
    try:
        wine_catalog = pandas.read_excel(
            io=wine_file,
            na_values='nan',
            keep_default_na=False
        )
    except FileNotFoundError:
        print(f"""Ошибка: Файл '{wine_file}' не найден!
        Укажите полный путь или проверьте файл""")
        sys.exit(1)

    wines = wine_catalog.to_dict('records')

    wine_cat = defaultdict(list)
    for wine in wines:
        category = wine.get('Категория')
        wine_cat[category].append(wine)

    for category in wine_cat:
        wine_cat[category].sort(
            key=lambda wine: wine.get('Цена', 0)
        )

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        wine_cat=wine_cat,
        years_old=format_age(age)
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print("Что бы остановить работу программы нажмите Ctrl + C")
    server.serve_forever()

if __name__ == "__main__":
    main()
