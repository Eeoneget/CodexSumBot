import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token, threaded=False)

total_expenses = 0

expense_categories = {
    "Такси": 0,
    "Дом": 0,
    "Транспорт": 0,
    "Еда": 0,
    "Развлечения": 0
}


def add_expense(message):
    global total_expenses

    if message.text in expense_categories:
        try:
            expense_value = float(message.text)
            expense_category = message.text
            expense_categories[expense_category] += expense_value
            total_expenses += expense_value
            bot.send_message(message.chat.id, text="Расход добавлен. Всего расходов: {}".format(total_expenses))
        except ValueError:
            bot.send_message(message.chat.id, text="Введите число")
            bot.register_next_step_handler(message, add_expense)
    else:
        bot.send_message(message.chat.id, text="Выберете один из предложенных видов расходов.")
        bot.register_next_step_handler(message, add_expense)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Посмотреть свои расходы")
    btn3 = types.KeyboardButton("Добавить расход")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я телеграмм бот для финансирования!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['choice'])
def choice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сколько я потратил за день?")
    btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
    btn3 = types.KeyboardButton("Сколько я потратил за месяц?")
    btn4 = types.KeyboardButton("Добавить расход")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, back)
    bot.send_message(message.chat.id, text="Посмотреть свои расходы", reply_markup=markup)


@bot.message_handler(commands=['help'])
def helping_hand(message):
    bot.send_message(message.chat.id, text='''Напишите (/choice) для того чтобы ввести сколько вы потратили''')


@bot.message_handler(content_types=['text'])
def func(message):

    global num, total_expenses

    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, text="""Привет Codex!
Напишите /help для того чтобы посмотреть доступные команды""")

    elif message.text == "Добавить расход":
        bot.send_message(message.chat.id, text="Введите сумму расхода:")
        bot.register_next_step_handler(message, add_expense)

    elif message.text == "Сколько я потратил за день?":
        today = int(total_expenses)
        bot.send_message(message.chat.id, text="Вы потратили {} за день".format(today))

    elif message.text == "Сколько я потратил за неделю?":
        week = int(total_expenses)
        bot.send_message(message.chat.id, text="Вы потратили {} за неделю".format(week))

    elif message.text == "Сколько я потратил за месяц?":
        month = int(total_expenses)
        bot.send_message(message.chat.id, text="Вы потратили {} за месяц".format(month))

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Посмотреть свои расходы")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    elif message.text == 'Добавить расход':
        bot.send_message(message.chat.id, text='Извините, эта функция находится в разработке')


bot.polling(none_stop=True)
