import collections
import datetime
import pandas

from pprint import pprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_actual_age():

    now = datetime.datetime.now()
    establish_year = 1920
    age = now.year - establish_year

    return age


def get_render_products_cards():

    excel_data_wines = pandas.read_excel('wine.xlsx')
    wines = excel_data_wines.to_dict(orient='record')

    return wines


def filter_products_categories():

    products_from_file = pandas.read_excel(
        'wine2.xlsx', na_values='nan', keep_default_na=False)
    products = products_from_file.to_dict(orient='record')

    filtered_products = collections.defaultdict(list)
    for product in products:
        category = product['Категория']
        filtered_products[category].append(product)

    return filtered_products


if __name__ == '__main__':

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    age = get_actual_age()
#    wines = get_render_products_cards()

    filtered_products = filter_products_categories()

    rendered_page = template.render(
        age=age, filtered_products=filtered_products)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
