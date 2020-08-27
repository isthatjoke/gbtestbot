from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler, BaseFilter)
from telegram.utils import helpers
from weather import *
import time, collections, logging, telegram, datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO) # error handler, avoid stopping bot after getting an error

updater = Updater(token='1337111137:AAELaRg_ixU9Wnx7FYmjXL2TkL1XCAssCUQ', use_context=True)
dispatcher = updater.dispatcher
last_conversation_about_city = collections.deque() # using deque to handle correct queries of weather reply_messages


def start(update, context):
    name = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, " + name + "! Я новый бот и в "
                                                                                        "данный момент "
                                                                                        "я пока что умею "
                                                                                        "только сообщать погоду в "
                                                                                        "Вашем городе.\n"
                                                                                        "Введите команду /weather.")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def ask_weather(update, context):
    button_location = telegram.InlineKeyboardButton(text='Геолокация', callback_data='weather_loc')
    button_city = telegram.InlineKeyboardButton(text='Ввести название города', callback_data='weather_key')
    keyboard = [[button_city], [button_location]]
    reply = telegram.InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Как сообщите город?",
                             reply_markup=reply)


def weather_button(update, context):
    query = update.callback_query
    if query.data == 'weather_loc':
        geo_request(update, context)
    if query.data == 'weather_key':
        message = context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите город..."
                                                                                  "пока есть Мск, Питер, Екат и Самара",
                                           reply_markup=telegram.ForceReply())
        return last_conversation_about_city.append(message)


def geo_request(update, context):
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
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.effective_chat.id, text=weather_coord, reply_markup=reply_markup)


def reply_city(update, context):
    for i in last_conversation_about_city:
        if update.message.reply_to_message.message_id == i['message_id']:
            weather_text = choose_the_city(update.message.text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=weather_text)
            last_conversation_about_city.remove(i)
            break


def unknown(update, context):
    """
    Message handler for unknown text messages
    :param update:
    :param context:
    :return:
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ничего пока не понимаю")


def job_empty_city_history(context: telegram.ext.CallbackContext):
    """
    Job starts at the moment the bot has been started and iterate the list of weather reply_messages deque every 30 sec.
    If it has data older than 5 min, data will be erased.
    :param context:
    :return:
    """
    for i in last_conversation_about_city:
        my_time = int(time.time())
        message_time = telegram.utils.helpers.to_timestamp(i['date'])
        if (my_time - message_time) > 300:
            last_conversation_about_city.remove(i)


job_cleaner = updater.job_queue.run_repeating(job_empty_city_history, interval=30, first=0)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.reply), echo)
dispatcher.add_handler(echo_handler)

geo_handler = CommandHandler('weather', ask_weather)
dispatcher.add_handler(geo_handler)

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

ask_weather_handler = CallbackQueryHandler(weather_button)
dispatcher.add_handler(ask_weather_handler)

reply_city_handler = MessageHandler(Filters.reply, reply_city)
dispatcher.add_handler(reply_city_handler)

if __name__ == '__main__':
    updater.start_polling()
