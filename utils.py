from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Прислать бегемотика'],
                                        [contact_button, location_button] 
                                      ], resize_keyboard=True
                                     )
    return my_keyboard


