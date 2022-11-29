import telebot
import configure
import datetime as dt
from math import *
from cmath import *

bot = telebot.TeleBot(configure.config['token'])

value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton('sqrt', callback_data='sqrt'),
                telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('del', callback_data='del'),
                telebot.types.InlineKeyboardButton('/', callback_data='/') )

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'),
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*') )

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='4'),
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-') )

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'),
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+') )

keyboard.row(   telebot.types.InlineKeyboardButton('00', callback_data='00'),
                telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data='.'),
                telebot.types.InlineKeyboardButton('=', callback_data='=') )

@bot.message_handler(commands=['start','calculator'])
def get_message(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == 'del':
        if value != '':
            value = value[:len(value)-1]
    elif data == 'sqrt':
        if value != '':
            value = str(sqrt(float(value)))
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'error'
    else:
        value += data

    if ( value != old_value and value != '' ) or ( '0' != old_value and value == '' ):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keyboard)
            old_value = value

    if value == 'error': value = ''

# ---------------------------------------------

@bot.message_handler(content_types=['text'])
def send_text(message):
    with open('logs.log', 'a') as data:
        time = dt.datetime.today().replace(microsecond=0)
        data.writelines(f"{time}\n")
        data.writelines(f" {message.from_user.first_name}: {message.text}\n")

bot.polling(none_stop=True, interval=0)