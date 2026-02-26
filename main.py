import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

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
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    template = env.get_template('template.html')
    
    rendered_page = template.render(
        years_old=age_format(age)
    )
    
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

if __name__ == "__main__":
    main()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print("Server started on http://0.0.0.0:8000")
    server.serve_forever()