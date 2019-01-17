from telegram.ext import Updater, CommandHandler
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


updater = Updater('268340955:AAH2VAP-MSirp68M64WvfqJTsqSj8wxzzic')
dispatcher = updater.dispatcher


def echo(bot, update):
    print(type(update))
    
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
