import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS
from config import TOKEN

count = 0
n = requests.Session()
news = requests.get('https://gimnaziya-17.dagestanschool.ru/news')
news_bs = BS(news.content, 'html.parser')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новости')
    item4 = types.KeyboardButton('/start')
    markup.add(item1, item4)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, чем вам помочь?'.format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def chat(message):
    global count
    if message.chat.type == 'private':
        if message.text == 'Новости':
            bot.send_message(message.chat.id, 'Новости:')
            for el in news_bs.select('.list-item'):
                title = el.select('.caption > a')
                date = el.select('.date > p')
                a = str(title[0]).index('"')
                bot.send_message(message.chat.id, date[0].text + ' - ' + title[0].text.strip() +
                                 ' - ' + 'https://gimnaziya-17.dagestanschool.ru/' + str(title[0])[a + 1:25])

        else:
            if count == 0:
                bot.send_message(message.chat.id, 'Нажмите нужную кнопку!')
                count += 1
            else:
                bot.send_message(message.chat.id, 'Вы что кнопки не видите?')


bot.polling(none_stop=True)

