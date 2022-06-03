from os import path, mkdir
from shutil import copytree, rmtree
from datetime import datetime
import codecs

from jinja2 import Environment, PackageLoader
import yaml

OUTPUT = 'output'
STATIC = 'static'

with open('pages.yaml') as f:
    pages = yaml.load(f, Loader=yaml.BaseLoader)

env = Environment(loader=PackageLoader('generate'))

if path.exists(OUTPUT):
    rmtree(OUTPUT)

mkdir(OUTPUT)

with open('.git/HEAD') as f:
    _, ref = f.read().rstrip().split(' ', 1)

with open('.git/' + ref) as f:
    commit = f.read().rstrip()

for page in pages:
    if not page['file'].endswith('.html'):
        continue
    template = env.get_template(page['file'])
    html = template.render(pages=pages, active=page, timestamp=datetime.now(),
            commit=commit)
    with codecs.open(path.join(OUTPUT, page['file']), 'wb', 'utf-8') as f:
        f.write(html)

copytree(STATIC, path.join(OUTPUT, STATIC))
