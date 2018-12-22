from glob import glob
import logging
from random import choice


import apiai, json
import datetime
from emoji import emojize
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton


import settings


date = datetime.datetime.now()
timeis_now = date.strftime('%Y/%m/%d')

m = ephem.Mars(timeis_now)
me = ephem.Mercury(timeis_now)
v = ephem.Venus(timeis_now)
j = ephem.Jupiter(timeis_now)
s = ephem.Saturn(timeis_now)
u = ephem.Uranus(timeis_now)
n = ephem.Neptune(timeis_now)
p = ephem.Pluto(timeis_now)






logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    text = 'Привет {}!'.format(emo)
    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())

def get_planet(bot, update):
    planet = update.message.text.split()
    print(planet[1])
    if planet[1] == 'Mars':
        text = ephem.constellation(m)
    elif planet[1] == 'Mercury':
        text = ephem.constellation(me)
    elif planet[1] == 'Venus':
        text = ephem.constellation(v)
    elif planet[1] == 'Jupiter':
        text = ephem.constellation(j)
    elif planet[1] == 'Saturn':
        text = ephem.constellation(s)
    elif planet[1] == 'Uranus':
        text = ephem.constellation(u)
    elif planet[1] == 'Neptune':
        text = ephem.constellation(n)
    elif planet[1] == 'Pluto':
        text = ephem.constellation(p)
    else:
        text = "Введите название планеты, а не это: {}".format(update.message.text)
    update.message.reply_text(text, reply_markup=get_keyboard())



def talk_to_me(bot, update, user_data):
    request = apiai.ApiAI('04384b48e7ae4b908c946b8de898c840').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'SmirnovAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=get_keyboard())
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!', reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    emi = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    print(update.message.contact)
    update.message.reply_text('Наберу на днях {}'.format(emi), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    emi = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    print(update.message.location)
    update.message.reply_text('Выезжаем {}'.format(emi), reply_markup=get_keyboard())


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Прислать бегемотика'],
                                        [contact_button, location_button] 
                                      ], resize_keyboard=True
                                     )
    return my_keyboard

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/tar*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def send_badikov(bot, update, user_data):
    bad_list = glob('images/bad*.jp*g')
    bad_pic = choice(bad_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(bad_pic, 'rb'), reply_markup=get_keyboard())

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(CommandHandler("tar4i", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать бегемотика)$', send_badikov, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))      
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()


main()