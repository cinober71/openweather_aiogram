import requests
import datetime
from aiogram import Bot, types
from config import open_weather_token, tg_bot_token
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привіт! Напиши мені назву міста і я пришлю прогноз погоди! \n "
                        f"Або ж я можу знайти погоду за твоїм місцемзнаходження за командою  /locate")


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Поділитись місцем знаходження", request_location=True)
    keyboard.add(button)
    return keyboard

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = round(message.location.latitude, 3)
    lon = (message.location.longitude)
    reply = "Погода за координатами : {}\n {}".format(lat, lon)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дождливо \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        print(data)
        city = data["name"]
        cur_weather = data["main"]["temp"]
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        print(lon, lat)
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись у вікно, а то не розумію яка погода!"
#co
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nШвидкість вітру: {wind} м/с\n"
                            f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                            f"***Хорошого дня!***"
                            )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


@dp.message_handler(commands=['locate'])
async def cmd_locate_me(message: types.Message):
    reply = "Натисніть на кнопку, щоб отримати погоду за вашим місцемзнаходження \n"
    await message.answer(reply, reply_markup=get_keyboard())

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дождливо \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        print(data)
        city = data["name"]
        cur_weather = data["main"]["temp"]
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        print(lon, lat)
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись у вікно, а то не розумію яка погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nШвидкість вітру: {wind} м/с\n"
              f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
              f"***Хорошого дня!***"
              )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)