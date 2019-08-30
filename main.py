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
        return "https://www.dropbox.com/s/vgmu1y5td37gomo/sunny.png?dl=0"

    elif weather_status == "broken clouds":
        return "https://www.dropbox.com/s/85y0wq8n5i854nr/cloud.png?dl=0"

    elif weather_status == "shower rain":
        return "https://www.dropbox.com/s/javtm9jreh2nyyy/rain.png?dl=0"

    else:
        return "https://www.dropbox.com/s/sgmud1o7i06dr7x/N_A.png?dl=0"

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
        try:
            city = message.text
            observation = owm.weather_at_place(city)
            w = observation.get_weather()
            temperature=w.get_temperature('celsius')['temp']
            detailed_status = w.get_detailed_status()

            bot.send_photo(
                message.from_user.id,get_weather_ico(detailed_status),
                "In " + city + " city air temperature " + str(int(temperature)) + " degrees Celsius and " + detailed_status + "\n" + choose_wear(temperature))
        except Exception:
            bot.send_message(message.from_user.id,"Enter corect city!")

#метод для постійної перевірки ботом чату
bot.polling(none_stop=True, interval=0)