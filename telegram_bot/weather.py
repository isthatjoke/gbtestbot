import requests

api = '57e77fa67b7f1374ba14b7f5022bfff1'
#city = input('Укажите город: ')

class Weather():
    weather_answer = ''
    weather_coord_answer = ''
    def __init__(self, city, lat, lon):
        self.city = city
        self.lat = lat
        self.lon = lon


    # def translate_weather(self, weather_answer):
    #     translate_answer = f'Погода в городе {weather_answer["name"]} {weather_answer["main"]["temp"]} градусов, '
    #       f'{weather_answer["weather"][0]["description"]}'
    #     return translate_answer

    def get_weather(self, city):
        main_get = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city + '&lang=ru&' \
                   'units=metric&appid=' + api
        weather_answer = requests.post(main_get).json()
        weather_answer = f'Погода в городе {weather_answer["name"]} {weather_answer["main"]["temp"]} градусов,' \
                 f' {weather_answer["weather"][0]["description"]}'
        return weather_answer

    def weather_by_coord(self, lat, lon):
        main_get = 'http://api.openweathermap.org/data/2.5/weather?lat=' + self.lat + '&lon=' + self.lon + \
                   '&lang=ru&units=metric&appid=' + api
        weather_answer = requests.post(main_get).json()
        temp = weather_answer["main"]["temp"]
        temp = float('{:.1f}'.format(temp))
        weather_coord_answer = f'Погода в городе {weather_answer["name"]} {temp} градусов,' \
                         f' {weather_answer["weather"][0]["description"]}'
        return weather_coord_answer



cities = {
    "москва": "moscow",
    "екатеринбург": "ekaterinburg",
    "екат": "ekaterinburg",
    "екб": "ekaterinburg",
    "ебург": "ekaterinburg",
    "самара": "samara",
    "питер": "saint petersburg",
    "санкт-петербург": "saint petersburg",
    "спб": "saint petersburg",
}


def choose_the_city(text):
    Weather.city = text.lower()
    if Weather.city in cities:
        Weather.city = cities[Weather.city]
        return Weather.get_weather(Weather, Weather.city)
    else:
        return f'Город указан некорректно или его пока нет в списке'


def get_coord(lat, lon):
    Weather.lat = lat
    Weather.lon = lon
    return Weather.weather_by_coord(Weather, Weather.lat, Weather.lon)

a = Weather.weather_answer
b = Weather.weather_coord_answer

if __name__ == "__main__":
   choose_the_city()
   weather_answer = a
   get_coord()
   weather_coord = b



