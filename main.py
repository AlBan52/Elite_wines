from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas

now = datetime.datetime.now()
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

excel_data_wines = pandas.read_excel(
    'C:/Users/AlBan/Desktop/wine_bugs/wine.xlsx')
wines = excel_data_wines.to_dict(orient='record')
template = env.get_template('C:/Users/AlBan/Desktop/wine_bugs/template.html')


rendered_page = template.render(
    age=now.year - 1920,
    wines=wines
)


with open('C:/Users/AlBan/Desktop/wine_bugs/index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
