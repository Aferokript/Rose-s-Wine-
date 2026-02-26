from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv


def count_wine_time(current_date):
    maked_wine = datetime.datetime(year=1920, month=11, day=24)
    return (current_date - maked_wine).days // 365


def fix_word_format(years):
    if 11 <= years % 100 <= 14:
        word = 'Лет'
    elif years % 10 == 1:
        word = 'Год'
    elif years% 10 == 2 or years % 10 == 3 or years % 10 == 4:
        word = 'Года'
    else:
        word = 'Лет'
    return word


def read_excel(file_path):
    excel_wine = pandas.read_excel(file_path)
    excel_dict = excel_wine.to_dict('records')
    wine_dict = collections.defaultdict(list)
    for wine in excel_dict:
        category = wine['Категория']
        wine_dict[category].append(wine)
    return wine_dict


def main():
    load_dotenv()
    current_date = datetime.datetime.today()
    years = count_wine_time(current_date)
    year_word = fix_word_format(years)
    
    # Передаем путь к файлу как параметр
    file_path = os.environ['KEEP_FILE']
    wine_dict = read_excel(file_path)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        wine_dict=wine_dict,
        year=years,
        year_word=year_word
    )

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()


