import hashlib
import json
import os
import dateutil.parser


def _ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)



def append_item(dir, item):
    _ensure_dir(dir)

    index = os.path.join(dir, 'index.json')
    with open(index, mode='a+', encoding='utf-8') as js:
        json.dump(item, js, ensure_ascii=False)
        js.write('\n')



def load_items(dir):
    name = os.path.join(dir, 'index.json')

    if not os.path.isfile(name):
        return []

    items = []

    #unique = set()
    with open(name, mode='r') as js:
        for line in js:
            if line:
                #if line in unique:
                #    continue
                #unique.add(line)

                item = json.loads(line)

                d = dateutil.parser.parse(item['time'])

                item['time'] = d
                item['date'] = d.date()

                items.append(item)
    return items
