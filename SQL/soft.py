import telebot
from telebot import types  # для указание типов
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Посмотреть свои расходы")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я телеграмм бот для финансирование!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Поздороваться"):
        bot.send_message(message.chat.id, text="Привет codex!")
    elif (message.text == "Выберите-"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сколько я потратил за день?")
        btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Посмотреть свои расходы", reply_markup=markup)

    elif (message.text == "Сколько я потратил за день?"):
        bot.send_message(message.chat.id, text="?")

    elif (message.text == "Сколько я потратил за неделю?"):
        bot.send_message(message.chat.id, text="?")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Посмотреть свои расходы")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling(none_stop=True)

