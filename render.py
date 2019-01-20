import os
from itertools import groupby
from shutil import copyfile

import db

__root = 'www'


def set_www_root(root):
    global __root
    __root = root


def render_context(context):
    items = db.load_items(context)

    items.sort(key=lambda x: x['time'])

    www_dir = os.path.join(__root, context)

    if not os.path.exists(www_dir):
        os.makedirs(www_dir)

    index_file = os.path.join(www_dir, 'index.html')

    data_dir = db.get_dir(context)

    with open(index_file, mode='w', encoding='utf-8') as w:
        w.write('<!DOCTYPE html>\n<html>')
        w.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        w.write('<link rel="stylesheet" type="text/css" href="/style.css">')
        w.write('<body>')
        for k, g in groupby(items, lambda x: x['date']):
            w.write('<h1>{0}</h1>\n'.format(k))
            for i in g:
                if i['kind'] == 'text':
                    lines = i['text'].split('\n')
                    for l in lines:
                        w.write('<p>' + l + '</p>\n')
                if i['kind'] == 'photo':
                    file = i['file']

                    dest_file = www_dir + "/" + file
                    if not os.path.exists(dest_file):
                        copyfile(data_dir + "/" + file, dest_file)
                    w.write("<img src='{0}'>\n".format(file))

        w.write('</body></html>')
