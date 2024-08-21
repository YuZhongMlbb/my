import telebot
from telebot import types
import requests
from config import TOKEN,API
from bs4 import BeautifulSoup

class News():

    def __init__(self) -> None:
        self.url = 'https://ria.ru/'
    
    def parse(self):
        r = requests.get(url=self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('span', class_="cell-list__item-title")

        for elem in items:
            yield elem.text

bot = telebot.TeleBot(TOKEN)
news = News()
n = news.parse()

@bot.message_handler(commands=['start'])


def first(message):


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Поиск','Команды')

    bot.send_message(message.chat.id,'Привет {}'.format(message.from_user.username),reply_markup=markup)


@bot.message_handler(commands=['город'])

def city(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Бишкек','Москва','Алматы','/назад')
    bot.send_message(message.chat.id,"Выберите город для получения информацции о погоде",reply_markup=markup)

@bot.message_handler(commands=['стоп'])

def stop(message):
    remove_markup =types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,'До новых встреч',reply_markup=remove_markup)

@bot.message_handler(commands=['новости'])

def news(message):
    bot.send_message(message.chat.id, f"Новость: {next(n)}")

@bot.message_handler(commands=['назад'])

def back(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Поиск','Команды')
        bot.send_message(message.chat.id,'И снова здравствуйте {}'.format(message.from_user.username),reply_markup=markup)

@bot.message_handler(content_types=['text'])

def get_text(message):
    if message.text == 'Команды':
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
          markup.row('/город','/стоп','/назад', '/новости')
          bot.send_message(message.chat.id,'Выбкри команду',reply_markup=markup)
    elif message.text == 'Поиск':
         bot.send_message(message.chat.id,'<b>выберите город</b>',parse_mode='html')
    else:
        try:
              file = open('weather.txt','w')
              CITY = message.text
              URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}"
              data = requests.get(url = URL)
              file.write(data.text)
              responce = requests.get(url=URL).json()
              info = {
                   'city':CITY,
                   'temp':responce['main']['temp'],
                   'weather': responce['weather'][0]['description'],
                   'wind':responce['wind']['speed']
              }
              bot.send_message(message.chat.id, f"{info}")
        except:
            print('Ошибка')

bot.polling(non_stop=True)