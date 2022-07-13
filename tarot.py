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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    my_channel_id = -1001518496730
    statuss = ['creator', 'administrator', 'member']
    for i in statuss:
        if i == bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status:
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Задать мне вопрос", callback_data = 'question_callback')
            keyboard.add(button)
            if message.chat.username != None:
                bot.send_message(message.chat.id, f"Привет, @{message.chat.username}! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                bot.send_message(message.chat.id, f"Привет, `{message.chat.first_name}`! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)
            break
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Подписаться ↗️", url = 'https://t.me/tarot_damn')
        done = types.InlineKeyboardButton(text = "Я подписался ✅", callback_data = 'done')
        keyboard.row(button)
        keyboard.row(done)
        bot.send_message(message.chat.id, "Подпишись на канал *«Личный советник»* для продолжения", parse_mode = 'Markdown', reply_markup = keyboard)

@bot.message_handler(commands = ['help_'])
def help(message):
    user_id = message.chat.id
    my_channel_id = -1001518496730
    statuss = ['creator', 'administrator', 'member']
    for i in statuss:
        if i == bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status:
            bot.reply_to(message, help_msg)
            break
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Подписаться ↗️", url = 'https://t.me/tarot_damn')
        done = types.InlineKeyboardButton(text = "Я подписался ✅", callback_data = 'done')
        keyboard.row(button)
        keyboard.row(done)
        bot.send_message(message.chat.id, "Подпишись на канал *«Личный советник»* для продолжения", parse_mode = 'Markdown', reply_markup = keyboard)
    

@bot.message_handler(commands = ['question'])
def question(message):
    user_id = message.chat.id
    my_channel_id = -1001518496730
    statuss = ['creator', 'administrator', 'member']
    for i in statuss:
        if i == bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status:
            bot.send_message(message.chat.id, "*Напиши свой вопрос, а я дам тебе на него ответ...*", parse_mode = 'Markdown')
            bot.register_next_step_handler(message, get_message)    
            break
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Подписаться ↗️", url = 'https://t.me/tarot_damn')
        done = types.InlineKeyboardButton(text = "Я подписался ✅", callback_data = 'done')
        keyboard.row(button)
        keyboard.row(done)
        bot.send_message(message.chat.id, "Подпишись на канал *«Личный советник»* для продолжения", parse_mode = 'Markdown', reply_markup = keyboard)
    

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'question_callback':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "*Напиши свой вопрос, а я дам тебе на него ответ...*", parse_mode = 'Markdown')
            bot.register_next_step_handler(call.message, get_message)
        elif call.data == 'done':
            user_id = call.message.chat.id
            my_channel_id = -1001518496730
            statuss = ['creator', 'administrator', 'member']
            for i in statuss:
                if i == bot.get_chat_member(chat_id = my_channel_id, user_id = call.message.chat.id).status:
                    keyboard = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton(text = "Задать мне вопрос", callback_data = 'question_callback')
                    keyboard.add(button)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f"Привет, `{call.message.chat.username}`! Я бот, который раскладывает карты 24/7 и способен ответить на твой любой вопрос в формате `да/нет`. Задай мне подходящий вопрос и я определю твою судьбу в один миг!\n\n*Пример:* `Меня завтра позовут на собеседование?`", parse_mode = 'Markdown', reply_markup = keyboard)
                    break
            else:
                bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Подписки на канал не обнаружено ❗️") 
                        

@bot.message_handler(commands = ['donate'])
def donationalerts(message):
    bot.send_message(message.from_user.id, 'Поддержать автора можно, *отправив любой донат* на QIWI/ЮMoney-кошелёк ❤️\nРеквизиты:\n• QIWI: `qiwi.com/n/TILYI849`\n• ЮMoney: `4100117470392066`\n\nПо поводу *платных* раскладов писать @whomet.', parse_mode = 'Markdown')
    bot.register_next_step_handler(message, get_message)
    
def get_message(message):
    user_id = message.chat.id
    my_channel_id = -1001518496730
    statuss = ['creator', 'administrator', 'member']
    for i in statuss:
        if i == bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status:
            id = message.text
            if id[0] != "/":
                yes = randint(0, 1)
                if yes == 1:
                    question = "`Да`"
                else:
                    question = "`Нет`"
                bot.send_message(message.chat.id, f"Ответ карт: {question}\nИ помни — карты *никогда* не врут!\n\nЧтобы задать ещё вопрос — просто напиши его в чат.\nЕсли какие-то команды *не сработали* — вызови их второй раз. ", parse_mode = 'Markdown')
                bot.register_next_step_handler(message, get_message)    
            break
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Подписаться ↗️", url = 'https://t.me/tarot_damn')
        done = types.InlineKeyboardButton(text = "Я подписался ✅", callback_data = 'done')
        keyboard.row(button)
        keyboard.row(done)
        bot.send_message(message.chat.id, "Подпишись на канал *«Личный советник»* для продолжения", parse_mode = 'Markdown', reply_markup = keyboard)
        
bot.polling(none_stop = True)
