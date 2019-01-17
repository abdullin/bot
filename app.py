import pytz
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler

local_tz = pytz.timezone('Asia/Yekaterinburg')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


updater = Updater('268340955:AAH2VAP-MSirp68M64WvfqJTsqSj8wxzzic')
dispatcher = updater.dispatcher


def echo(bot, update: Update):
    print(type(update))
    m : Message = update.message
    print(utc_to_local(update.message.date))


    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
