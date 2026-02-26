import datetime
import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint
from collections import defaultdict

def company_age():
    return datetime.date.today().year - 1920


def age_format(years):
    if 11 <= years % 100 <= 19:
        return f"{years} лет"
    elif years % 10 == 1:
        return f"{years} год"
    elif 2 <= years % 10 <= 4:
        return f"{years} года"
    else:
        return f"{years} лет"


def main():
    age = company_age()
    wine_catalog = pandas.read_excel(io='wine2.xlsx', na_values='nan', keep_default_na=False)
    wines = wine_catalog.to_dict('records')
    wine_cat = defaultdict(list)  
    for wine in wines:
        category = wine['Категория']
        wine_cat[category].append({
            'Название': wine['Название'],
            'Сорт': wine['Сорт'],
            'Цена': wine['Цена'],
            'Картинка': wine['Картинка']
        })
    
    pprint(wine_cat)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    template = env.get_template('template.html')
    
    rendered_page = template.render(
        wines=wines,
        wine_categories=dict(wine_cat),
        years_old=age_format(age)
    )
    
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

if __name__ == "__main__":
    main()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
