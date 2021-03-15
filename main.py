import datetime
import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_actual_age():

    now = datetime.datetime.now()
    establish_year = 1920
    rendered_page = template.render(
        now.year - establish_year,
        wines=wines
    )
    return rendered_page


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

excel_data_wines = pandas.read_excel('wine.xlsx')
wines = excel_data_wines.to_dict(orient='record')
template = env.get_template('template.html')


if __name__ == '__main__':

    get_actual_age()
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
