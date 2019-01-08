from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
from telegram import ReplyKeyboardMarkup
from emoji import emojize

from random import choice
from glob import glob

import logging
import settings
import datetime
import ephem

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
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {}!'.format(emo)
    logging.info(text)
    update.message.reply_text(text)

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
    update.message.reply_text(text)



def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = 'Привет, {} {}! Ты написал: {}'.format(update.message.chat.first_name, emo, update.message.text) 
    logging.info("User: %s, Message: %s, Chat: %s", update.message.chat.username, update.message.text, update.message.chat.id)
    update.message.reply_text(user_text)

def send_cat_picture(bot, update):
    cat_list = glob('images/tar*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']
   

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()