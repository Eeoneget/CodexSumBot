import sqlite3
import telebot
from telebot import types
import config
from datetime import datetime, timedelta

bot = telebot.TeleBot(config.token, threaded=False)

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Создаем таблицу расходов, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()


def sum_expenses(user_id, period):
    # Вычисляем сумму расходов за указанный период для данного пользователя
    query = "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND timestamp >= ?"

    if period == "day":
        period_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        period_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
            days=datetime.now().weekday())
    elif period == "month":
        period_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    cursor.execute(query, (user_id, period_start))
    result = cursor.fetchone()[0]

    if result is not None:
        return result
    else:
        return 0


def add_expense(message):
    try:
        user_id = message.from_user.id
        amount = float(message.text)
        cursor.execute("INSERT INTO expenses (user_id, amount) VALUES (?, ?)", (user_id, amount))
        conn.commit()
        bot.send_message(message.chat.id,
                         text="Расход добавлен. Всего расходов за день: {}".format(sum_expenses(user_id, "day")))
    except ValueError:
        bot.send_message(message.chat.id, text="Введите число")
        bot.register_next_step_handler(message, add_expense)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сколько я потратил за день?")
    btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
    btn3 = types.KeyboardButton("Сколько я потратил за месяц?")
    btn4 = types.KeyboardButton('Добавить расход')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="""Привет, {0.first_name}! Напишите /expenses, чтобы посмотреть сколько ты потратил""".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['choice'])
def choice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сколько я потратил за день?")
    btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
    btn3 = types.KeyboardButton("Сколько я потратил за месяц?")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, back)
    bot.send_message(message.chat.id, reply_markup=markup)


@bot.message_handler(commands=['expenses'])
def view_expenses(message):
    user_id = message.from_user.id
    today = sum_expenses(user_id, "day")
    week = sum_expenses(user_id, "week")
    month = sum_expenses(user_id, "month")

    response = "Суммарные расходы:\n\n"
    response += "За день: {}\n".format(today)
    response += "За неделю: {}\n".format(week)
    response += "За месяц: {}\n".format(month)

    bot.send_message(message.chat.id, text=response)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Меню":
        bot.send_message(message.chat.id, text="""Привет! Напишите /expenses, чтобы посмотреть сколько ты потратил""")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сколько я потратил за день?")
        btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
        btn3 = types.KeyboardButton("Сколько я потратил за месяц?")
        btn4 = types.KeyboardButton('Добавить расход')
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Посмотреть свои расходы", reply_markup=markup)
    elif message.text == "Добавить расход":
        bot.send_message(message.chat.id, text="Введите сумму расхода:")
        bot.register_next_step_handler(message, add_expense)

    elif message.text == "Сколько я потратил за день?":
        user_id = message.from_user.id
        today = sum_expenses(user_id, "day")
        bot.send_message(message.chat.id, text="Вы потратили {} за день".format(today))

    elif message.text == "Сколько я потратил за неделю?":
        user_id = message.from_user.id
        week = sum_expenses(user_id, "week")
        bot.send_message(message.chat.id, text="Вы потратили {} за неделю".format(week))

    elif message.text == "Сколько я потратил за месяц?":
        user_id = message.from_user.id
        month = sum_expenses(user_id, "month")
        bot.send_message(message.chat.id, text="Вы потратили {} за месяц".format(month))

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button3 = types.KeyboardButton('Добавить расход')
        markup.add(button1,  button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)


bot.polling(none_stop=True)
