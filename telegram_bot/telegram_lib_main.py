import telegram
from telegram.ext import Updater
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters)
from weather import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='1337111137:AAELaRg_ixU9Wnx7FYmjXL2TkL1XCAssCUQ', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я новый бот и в данный момент "
                                                                    "я пока что умею только сообщать погоду в "
                                                                    "Вашем городе.\n"
                                                                    "Введите команду /weather.")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def geo(update, context):
    geo_button = telegram.KeyboardButton(text='Поделиться локацией', request_location=True)
    keyboard = [[geo_button]]
    reply = telegram.ReplyKeyboardMarkup(keyboard, row_width=1, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Подскажите Ваше местоположение",
                             reply_markup=reply)


def location(update, context):
    coord = update.message.location
    lat = str(coord['latitude'])
    lon = str(coord['longitude'])
    weather_coord = get_coord(lat, lon)
    context.bot.send_message(chat_id=update.effective_chat.id, text=weather_coord)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ничего пока не понимаю")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

geo_handler = CommandHandler('weather', geo)
dispatcher.add_handler(geo_handler)

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)




if __name__ == '__main__':
    updater.start_polling()

