import requests


#city = input('Укажите город: ')

class Weather():
    def __init__(self, city):
        self.city = city


    def translate_weather(self, weather_answer):
        print(f'Погода в городе {weather_answer["name"]} {weather_answer["main"]["temp"]} градусов, '
          f'{weather_answer["weather"][0]["description"]}')

    def get_weather(self, city):
        main_get = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city + '&lang=ru&' \
                   'units=metric&appid=57e77fa67b7f1374ba14b7f5022bfff1'
        weather_answer = requests.post(main_get).json()
        answer =  self.translate_weather(self, weather_answer)
        return answer










if __name__ == "__main__":
    cities = {"москва": "moscow", "екатеринбург": "ekaterinburg", "самара": "samara"}
    Weather.city = (input("Укажите город: ").lower())
    if Weather.city in cities:
        Weather.city = cities[Weather.city]
    Weather.get_weather(Weather, Weather.city)

