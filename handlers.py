from emoji import emojize
from glob import glob
from random import choice
from utils import get_keyboard

import apiai, json
import logging
import settings


def greet_user(bot, update, user_data):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    text = 'Привет {}!'.format(emo)
    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    request = apiai.ApiAI(settings.API_AI).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'SmirnovAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=get_keyboard())
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Чего началось-то? Нормально же общались!', reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    emi = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    print(update.message.contact)
    update.message.reply_text('Наберу на днях {}'.format(emi), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    emi = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    print(update.message.location)
    update.message.reply_text('Выезжаем {}'.format(emi), reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/tar*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def send_badikov(bot, update, user_data):
    bad_list = glob('images/bad*.jp*g')
    bad_pic = choice(bad_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(bad_pic, 'rb'), reply_markup=get_keyboard())
