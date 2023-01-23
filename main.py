import telebot
from telebot import types
from tele_token import TOKEN
from create_db import create_db, get_data_by_profession, get_person_info
import random


# create&fill db
create_db()

bot = telebot.TeleBot(TOKEN, parse_mode=None)

def create_buttons(id):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Writer ✍')
    btn2 = types.KeyboardButton('Football Player ⚽')
    btn3 = types.KeyboardButton('Physicist ⚛🔭')
    markup.add(btn1, btn2, btn3)
    bot.send_message(id, "Please select profession", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	create_buttons(message.chat.id)
        
@bot.message_handler(content_types=['text'])
def response_text(message):
    if (message.text == 'Writer ✍'):
        people_list = get_data_by_profession('writer')
        person = random.choice(people_list)
        info = get_person_info(person)
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
    elif (message.text == 'Football Player ⚽'):
        people_list = get_data_by_profession('football player')
        person = random.choice(people_list)
        info = get_person_info(person)
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
    elif (message.text == 'Physicist ⚛🔭'):
        people_list = get_data_by_profession('physicist')
        person = random.choice(people_list)
        info = get_person_info(person)
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
    
bot.infinity_polling()