import json
import os
import dateutil.parser

__folder = os.path.abspath('data')


def _user_file_name(user_id):
    return os.path.join(__folder, "user-{0}.json".format(user_id))


def get_user_info(user_id):
    name = _user_file_name(user_id)

    if not os.path.isfile(name):
        return {}
    with open(name, mode='r') as js:
        return json.loads(js)


def save_user_info(user_id, info):
    name = _user_file_name(user_id)
    with open(name, mode='w', encoding='utf-8') as js:
        json.dump(info, js, ensure_ascii=False)


def _ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_dir(context):
    dir = os.path.join(__folder, context)
    _ensure_dir(dir)
    return dir


def append_item(context, item):
    dir = os.path.join(__folder, context)
    _ensure_dir(dir)

    index = os.path.join(dir, 'index.json')
    with open(index, mode='a+', encoding='utf-8') as js:
        json.dump(item, js, ensure_ascii=False)
        js.write('\n')


def load_items(context):
    name = os.path.join(__folder, context, 'index.json')

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
