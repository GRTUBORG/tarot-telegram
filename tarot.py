import telebot
import random
import httpx
import os
import time
import requests

from telebot import types
from random import randint

help_msg = """Приветствую, путник! Вот список моих магических команд:
• /question — задать мне вопрос;
• /help — вызвать это меню.

По поводу платных раскладов писать @whomet."""

token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text = "Задать мне вопрос", callback_data = 'question_callback')
    keyboard.add(button)
    bot.send_message(message.chat.id, f"Привет, @{message.chat.username}! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)

@bot.message_handler(commands = ['help'])
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
        bot.send_message(message.chat.id, f"Ответ карт: {question}\nИ помни — карты *никогда* не врут!\n\nЧтобы задать ещё вопрос — просто напиши его в чат", parse_mode = 'Markdown')
        bot.register_next_step_handler(message, get_message)
        
bot.polling(none_stop = True)