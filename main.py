import argparse
import collections
import datetime
import pandas

from collections import OrderedDict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_actual_age():

    now = datetime.datetime.now()
    establish_year = 1920
    age = now.year - establish_year
    digit_of_age = [int(digit) for digit in str(age)]
    first_digit, second_digit, last_digit = digit_of_age[0], digit_of_age[1], digit_of_age[2]

    if first_digit == 1 and second_digit != 1 and last_digit == 1:
        age_word = 'год'
    elif second_digit == 0 and last_digit >= 2 and last_digit <= 4:
        age_word = 'года'
    elif last_digit == 0 or last_digit >= 5 and last_digit <= 9:
        age_word = 'лет'
    else:
        age_word = 'лет'

    return age, age_word


def parse_products_from_file():

    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Full path to file with products')
    args = parser.parse_args()
    file_path = args.file_path

    products_from_file = pandas.read_excel(
        file_path, na_values='nan', keep_default_na=False)
    products = products_from_file.to_dict(orient='record')

    return products


def get_sorted_products(products):

    filtered_products = collections.defaultdict(list)
    for product in products:
        category = product['Категория']
        filtered_products[category].append(product)

    sorted_products = dict(sorted(filtered_products.items()))

    return sorted_products


if __name__ == '__main__':

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    age, age_word = get_actual_age()

    products = parse_products_from_file()

    sorted_products = get_sorted_products(products)

    rendered_page = template.render(
        age=age,
        sorted_products=sorted_products,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
