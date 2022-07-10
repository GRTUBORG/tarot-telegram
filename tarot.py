import telebot
import random
import os
import time
import requests

from telebot import types
from random import randint

help_msg = """Приветствую, путник! Вот список моих магических команд:
• /question — задать мне вопрос;
• /help_ — вызвать это меню.
Если какие-то команды не сработали — вызови их второй раз. 

По поводу платных раскладов писать @whomet."""

token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def welcome(message):
    str_countes = ''
    countes = [f'{message.from_user.id} — ID,\n',
               f'{message.from_user.first_name} — имя,\n',
               f'{message.from_user.last_name} — фамилия,\n',
               f'{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text = "Задать мне вопрос", callback_data = 'question_callback')
    keyboard.add(button)
    if message.chat.username != None:
        bot.send_message(message.chat.id, f"Привет, @{message.chat.username}! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        bot.send_message(message.chat.id, f"Привет, `{message.chat.first_name}`! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)
     
    bot.send_message(655041562, f'У тебя +1 новый пользователь! \n{str_countes}')
@bot.message_handler(commands = ['help_'])
def help(message):
    bot.reply_to(message, help_msg)

@bot.message_handler(commands = ['question'])
def question(message):
    bot.send_message(message.chat.id, "*Напиши свой вопрос, а я дам тебе на него ответ...*", parse_mode = 'Markdown')
    bot.register_next_step_handler(message, get_message)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'question_callback':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "*Напиши свой вопрос, а я дам тебе на него ответ...*", parse_mode = 'Markdown')
            bot.register_next_step_handler(call.message, get_message)

@bot.message_handler(commands = ['donate'])
def donationalerts(message):
    bot.send_message(message.from_user.id, 'Поддержать автора можно, *отправив любой донат* на QIWI/ЮMoney-кошелёк ❤️\nРеквизиты:\n• QIWI: `qiwi.com/n/TILYI849`\n• ЮMoney: `4100117470392066`\n\nПо поводу *платных* раскладов писать @whomet.', parse_mode = 'Markdown')
    bot.register_next_step_handler(message, get_message)
    
def get_message(message):
    id = message.text
    if id[0] != "/":
        yes = randint(0, 1)
        if yes == 1:
            question = "`Да`"
        else:
            question = "`Нет`"
        bot.send_message(message.chat.id, f"Ответ карт: {question}\nИ помни — карты *никогда* не врут!\n\nЧтобы задать ещё вопрос — просто напиши его в чат.\nЕсли какие-то команды *не сработали* — вызови их второй раз. ", parse_mode = 'Markdown')
        bot.register_next_step_handler(message, get_message)
        
bot.polling(none_stop = True)
