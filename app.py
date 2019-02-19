import argparse
import datetime
import hashlib
import json
import logging
import os
import subprocess
import sys
import traceback
from os import path
from threading import Thread

import pytz
from telegram import Update, Bot
from telegram.ext import Updater
import db

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description='Launch telegram bot')
parser.add_argument('--key', action='store', dest='key', required=True)
parser.add_argument('--store', action='store', dest='root', required=True)

# to allow introducing arguments in advance
cfg, unknown = parser.parse_known_args()

with open(os.path.join(cfg.root, "telegram.json")) as f:
    tg_cfg = json.load(f)

reply_chat_id = int(tg_cfg['reply_chat_id'])

local_tz = pytz.timezone('Asia/Yekaterinburg')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # .normalize might be unnecessary


updater = Updater(token=cfg.key)
dispatcher = updater.dispatcher
bot = updater.bot


def sha256sum(filename):
    h = hashlib.sha1()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def handle_message(bot: Bot, update: Update):
    context = ""
    try:

        message = update.effective_message
        chat_id = str(message.chat_id)

        if not chat_id in tg_cfg['chats']:
            reply("Chat {0} not registered".format(chat_id), message.chat_id)
            return

        chat = tg_cfg['chats'][chat_id]
        folder = chat['folder']

        context = folder

        local = get_message_date_local(update)

        dict = update.to_dict()

        em = dict.pop("_effective_message", None)

        del_empty_values(em)

        em.pop("chat", None)

        index_dir = path.join(cfg.root, folder)

        os.makedirs(index_dir, exist_ok=True)

        for kind in ['document', 'video']:
            resource = em.get(kind, None)
            if resource:
                save_file(resource, index_dir, context)
                thumb = resource.get('thumb')
                if thumb:
                    save_file(thumb, index_dir, context)

        photo = em.get("photo", None)
        if photo:
            save_file(photo[-1], index_dir, context)
            save_file(photo[-2], index_dir, context)

        em["_time"] = local.isoformat()
        em["update_id"] = update.update_id

        db.append_item(index_dir, em)

        exec = chat.get('exec', None)

        if not exec:
            reply("{0}> saved {1}".format(context, update.update_id))
            return

        result = subprocess.run(exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path.abspath(index_dir))
        output = result.stdout.decode('utf-8')
        if len(output) > 2000:
            output = output[-2000:]
        reply("{0}> exec {1} ret {2}: {3}".format(context, result.args, result.returncode, output))

    except:
        reply("{0}> err {1}".format(context, traceback.format_exc()))
        return


def del_empty_values(em):
    for k in list(em):
        if not em[k]:
            em.pop(k)


def save_file(doc, index_dir, context):
    file_id = doc['file_id']
    file = bot.get_file(file_id)

    temp_path = path.join(index_dir, "download.tmp")
    file.download(custom_path=temp_path)
    hash = sha256sum(temp_path)

    doc['sha1'] = hash
    basename = path.basename(file.file_path)
    doc['name'] = basename
    os.rename(temp_path, path.join(index_dir, hash))
    reply("{0}> saved {1} as {2}".format(context, basename, hash[0:7]))


def get_message_date_local(update: Update):
    message = update.effective_message
    date = message.date
    if message.forward_date:
        date = message.forward_date
    local: datetime.datetime = utc_to_local(date)
    return local


def reply(status, chat_id=None):
    bot.send_message(chat_id=chat_id or reply_chat_id, text=status)


from telegram.ext import MessageHandler, Filters

dispatcher.add_handler(MessageHandler(
    Filters.all,
    handle_message,
    allow_edited=True,
    message_updates=True))


def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    import time
    time.sleep(3600 * 2)
    print("Restarting the updater")
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


updater.start_polling()
# restart the process regularly
# working around weird behavior on vpn network changes
Thread(target=stop_and_restart, daemon=True).start()
updater.idle()
