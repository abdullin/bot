import os
from itertools import groupby
from shutil import copyfile

import context
import db

__root = 'www'


def set_www_root(root):
    global __root
    __root = root


def render_all():
    for c in context.list():
        render_context(c)


def render_context(context):
    items = db.load_items(context)

    items.sort(key=lambda x: x['time'])

    www_dir = os.path.join(__root, context)

    if not os.path.exists(www_dir):
        os.makedirs(www_dir)

    index_file = os.path.join(www_dir, 'index.html')

    data_dir = db.get_dir(context)

    with open(index_file, mode='w', encoding='utf-8') as w:
        w.write('<!DOCTYPE html>\n<html lang="en">\n')
        w.write('<head>\n')
        w.write('<meta charset="utf-8">\n')
        w.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')

        w.write('<link rel="stylesheet" type="text/css" href="/style.css">\n')
        w.write(
            '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">\n')
        w.write('</head>')
        w.write('<body>')
        w.write('<div class="container">')

        for k, g in groupby(items, lambda x: x['date']):

            w.write('<h1>{0}</h1>\n'.format(k))
            for i in g:
                w.write('<div class="row"><div class="col-12 justify-content-center col-md-8">\n')

                if i['kind'] == 'text':
                    lines = i['text'].split('\n')
                    for l in lines:
                        w.write('<p>' + l + '</p>\n')
                if i['kind'] == 'photo':

                    picked = None
                    for photo in i['photos']:
                        width = photo['width']

                        if not picked and width >= 800:
                            picked = photo

                        file = photo['file']
                        dest_file = www_dir + "/" + file
                        if not os.path.exists(dest_file):
                            copyfile(data_dir + "/" + file, dest_file)
                    if not picked:
                        picked = i['photos'][-1]

                    w.write("<img src='{0}'>\n".format(picked['file']))
                w.write('</div></div>') # row

        w.write('</div>\n')
        w.write('</body></html>')
