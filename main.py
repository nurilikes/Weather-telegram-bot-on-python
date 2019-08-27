# Telegram weather bot by
# ©Bogdan Yatsiv(@cprograme)
# 25.08.2019
# for SoftServe IT academy final project

import pyowm
import telebot

#API ключі
TG_TOKEN = "896910396:AAF9CU3XVOnNDsXT1T35uF9C21uMsjvMpdU"
owm = pyowm.OWM('ef2206ff5da67de63306d0b143e20872')

#ініціалізація бота
bot = telebot.TeleBot(TG_TOKEN)

def get_weather_ico(weather_status):
    if weather_status == "clear sky":
        photo = open("E:/Studie/PyPrograms/Chat projeckt/Python-chat/sunny.png","rb")
        return photo

    elif weather_status == "broken clouds":
        photo = open("E:/Studie/PyPrograms/Chat projeckt/Python-chat/cloud.png","rb")
        return photo

    elif weather_status == "shower rain":
        photo = open("E:/Studie/PyPrograms/Chat projeckt/Python-chat/rain.png","rb")
        return photo

    else:
        photo = open("E:/Studie/PyPrograms/Chat projeckt/Python-chat/N_A.png","rb")
        return photo

def choose_wear(temperature):
    if temperature >= 20:
        return "Take shorts and sunglases"

    elif temperature > 10 and temperature < 20:
        return "Take jacket or warm sweater"

    elif temperature < 10 and temperature > 0:
        return "It`s geting really cold, take warm socks from your grandma"

    elif temperature < 0:
        return "You should take down jacket and warm hat"

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id,"Hi, i`am weather bot.\nIf you have questions type /help\nIf you want to check weather type your city")

    elif message.text == "/help":
        bot.send_message(message.from_user.id,"Just type your city to get weather info")

    elif message.text == "kis kis kis":
        bot.send_photo(message.from_user.id,"https://images.app.goo.gl/ZxSvid8W78cTx2yk7")

    else:
        # перевіряємо погоду в місті
        city = message.text
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temperature=w.get_temperature('celsius')['temp']
        detailed_status = w.get_detailed_status()
        bot.send_message(message.from_user.id,"In " + city + " city air temperature " + str(int(temperature)) + " degrees Celsius and " + detailed_status)

        bot.send_message(message.from_user.id,choose_wear(temperature))

        bot.send_photo(message.from_user.id,get_weather_ico(detailed_status))



#метод для постійної перевірки ботом чату
bot.polling(none_stop=True, interval=0)