import telebot
from telebot import types  # для указанья типов
import config

bot = telebot.TeleBot(config.token, threaded=False)

num = 0
sum_num = 0
taxi_num = 0

expense_categories = {
    "Такси": 0.0,
    "Дом": 0.0,
    "Транспорт": 0.0,
    "Еда": 0.0,
    "Развлечения": 0.0,
    "Другое": 0.0,
}


def sum_expenses(period):
    # здесь должен быть код, который вычисляет сумму расходов за указанный период
    # в зависимости от значения параметра period
    # например, если period равен "day", то нужно вычислить сумму расходов за день
    # и вернуть это значение
    # если period равен "week", то нужно вычислить сумму расходов за неделю
    # и вернуть это значение
    # и т.д.
    return sum_num


def add_expense(message):
    if message.text == 'Такси':
        global num, sum_num
        try:
            num_taxi = float(input())
            expense_categories['Такси'] = expense_categories['Такси'] + num_taxi
            bot.send_message(message.chat.id, text="Расход добавлен. Всего расходов На такси: {}".format(num_taxi))
        except ValueError:
            bot.send_message(message.chat.id, text="Введите число")
            bot.register_next_step_handler(message, add_expense)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Посмотреть свои расходы")
    btn3 = types.KeyboardButton("Добавить расход")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я телеграмм бот для финансирование!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['choice'])
def choice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сколько я потратил за день?")
    btn2 = types.KeyboardButton("Сколько я потратил за неделю?")
    btn3 = types.KeyboardButton("Сколько я потратил за месяц?")
    btn4 = types.KeyboardButton('Добавить расход')
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, back)
    bot.send_message(message.chat.id, text="Посмотреть свои расходы", reply_markup=markup)


@bot.message_handler(commands=['help'])
def helping_hand(message):
    bot.send_message(message.chat.id, text='''Напишите /choice для того чтобы ввести сколько вы потратили''')


@bot.message_handler(content_types=['text'])
def func(message):
    global num, sum_num
    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, text="""Привет Codex!
Напишите /help для того чтобы посмотреть доступные команды""")
    elif message.text == "Сколько я потратил за день?":
        today = sum_expenses("day")
        bot.send_message(message.chat.id, text="Вы потратили {} за день".format(today))

    elif message.text == "Сколько я потратил за неделю?":
        week = sum_expenses("week")
        bot.send_message(message.chat.id, text="Вы потратили {} за неделю".format(week))

    elif message.text == "Сколько я потратил за месяц?":
        month = sum_expenses("month")
        bot.send_message(message.chat.id, text="Вы потратили {} за месяц".format(month))

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Посмотреть свои расходы")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)


bot.polling(none_stop=True)
