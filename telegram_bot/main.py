import requests
import weather


#bot_api = 'https://api.telegram.org/bot1337111137:AAELaRg_ixU9Wnx7FYmjXL2TkL1XCAssCUQ/'
bot_token = '1337111137:AAELaRg_ixU9Wnx7FYmjXL2TkL1XCAssCUQ'
weather_api = '57e77fa67b7f1374ba14b7f5022bfff1'
#https://openweathermap.org/current


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.bot_api = f'https://api.telegram.org/bot{token}/'

    def get_updates(self, timeout = 20, offset = None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.bot_api + method, params)
        result = response.json()['result']
        return result

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        answer = requests.post(self.bot_api + method, params)
        return answer

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


bot = BotHandler(bot_token)

greetings = 'Привет! Я новый бот и в данный момент я пока что умею только сообщать погоду в Вашем городе.\n' \
            'Введите команду /weather'


def main():
    new_offset = None
    message_id = 0
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        last_update_id = last_update['update_id']
        last_command_type = last_update['message']['entities'][0]['type']
        last_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_message_id = last_update['message']['message_id']

        if last_command_type == 'bot_command' and last_text == '/start' and last_message_id != message_id:
            bot.send_message(last_chat_id, greetings)
            message_id = last_message_id
        elif last_command_type == 'bot_command' and last_text == '/weather':
            pass

        new_offset = last_update_id + 1





if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
