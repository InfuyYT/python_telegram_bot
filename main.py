import telebot
from telebot import types
from googletrans import Translator
import os
from dotenv import load_dotenv

load_dotenv()
secret_token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token=secret_token)

translator = Translator()

# Словарь для хранения языков
languages = {'en': 'английский', 'ru': 'русский'}
current_lang = {'source': 'en', 'target': 'ru'}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, мой друг! Я - твой верный переводчик, всегда готовый помочь тебе разобраться в мире языков. Я могу перевести с русского на английский и наоборот. Давай начнем работу вместе!', reply_markup=get_keyboard())

# Обработчик команды /change
@bot.message_handler(commands=['change'])
def change_language(message):
    # Меняем языки местами
    current_lang['source'], current_lang['target'] = current_lang['target'], current_lang['source']
    # Отправляем сообщение об изменении языка
    bot.send_message(message.chat.id, f'Язык перевода изменен на {languages[current_lang["source"]]} -> {languages[current_lang["target"]]}', reply_markup=get_keyboard())

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def translate_message(message):
    try:
        # Переводим сообщение на язык target
        translated = translator.translate(message.text, src=current_lang['source'], dest=current_lang['target'])
        print(message.text)
        # Отправляем перевод
        bot.send_message(message.chat.id, translated.text, reply_markup=get_keyboard())
        print(translated.text)
    except:
        # Если возникает ошибка при переводе, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, 'Произошла ошибка при переводе сообщения.', reply_markup=get_keyboard())

# Создание клавиатуры с командами
def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/start'), types.KeyboardButton('/change'))
    return keyboard

# Запуск бота
bot.polling()
