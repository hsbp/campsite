from os import path, mkdir
from shutil import copytree, rmtree
import codecs

from jinja2 import Environment, PackageLoader
import yaml

OUTPUT = 'output'
STATIC = 'static'

with open('pages.yaml') as f:
    pages = yaml.load(f)

env = Environment(loader=PackageLoader('__main__', 'templates'))

if path.exists(OUTPUT):
    rmtree(OUTPUT)

mkdir(OUTPUT)

for page in pages:
    template = env.get_template(page['file'])
    html = template.render(pages=pages, active=page)
    with codecs.open(path.join(OUTPUT, page['file']), 'wb', 'utf-8') as f:
        f.write(html)

copytree(STATIC, path.join(OUTPUT, STATIC))
