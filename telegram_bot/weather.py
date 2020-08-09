import requests


#city = input('Укажите город: ')

class Weather():
    weather_answer = ''
    def __init__(self, city):
        self.city = city


    # def translate_weather(self, weather_answer):
    #     translate_answer = f'Погода в городе {weather_answer["name"]} {weather_answer["main"]["temp"]} градусов, '
    #       f'{weather_answer["weather"][0]["description"]}'
    #     return translate_answer

    def get_weather(self, city):
        main_get = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city + '&lang=ru&' \
                   'units=metric&appid=57e77fa67b7f1374ba14b7f5022bfff1'
        weather_answer = requests.post(main_get).json()
        weather_answer = f'Погода в городе {weather_answer["name"]} {weather_answer["main"]["temp"]} градусов,' \
                 f' {weather_answer["weather"][0]["description"]}'
        return weather_answer

cities = {"москва": "moscow", "екатеринбург": "ekaterinburg","екат": "ekaterinburg", "самара": "samara"}

def choose_the_city(text):
    Weather.city = text.lower()
    if Weather.city in cities:
        Weather.city = cities[Weather.city]
        return Weather.get_weather(Weather, Weather.city)


a = Weather.weather_answer

if __name__ == "__main__":
   choose_the_city()
   weather_answer = a



