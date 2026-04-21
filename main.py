import os
import telebot
from dotenv import load_dotenv
from telebot.types import KeyboardButton
from all_db import Database
from random import randint
from test import start_test
from list import show_my_tests

load_dotenv(dotenv_path='.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
db = Database()
db.init_db()


def main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_test = KeyboardButton('Create Test 📋')
    delete_test = KeyboardButton('Delete Test 🗑')
    my_test = KeyboardButton('My Tests 📝')
    keyboard.add(create_test, delete_test)
    keyboard.add(my_test)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    if len(message.text.split()) > 1:
        unique_id = message.text.split()[1]
        start_test(bot, message, unique_id)
    else:
        bot.send_message(
            message.chat.id,
            f"Привет {message.from_user.first_name}!\n"
            f"Создай тест и отправь его друзьям",
            reply_markup=main_keyboard()
        )


@bot.message_handler(func=lambda message: message.text == 'Create Test 📋')
def set_name_test(message):
    msg = bot.send_message(
        message.chat.id,
        'Введите название теста:'
    )
    bot.register_next_step_handler(msg, count_questions)


@bot.message_handler(func=lambda message: message.text == 'My Tests 📝')
def my_tests(message):
    show_my_tests(bot, message)


def count_questions(message):

    user_data[message.chat.id] = {
        'name': message.text,
        'count': 0,
        'questions_done': 0,
        'unique_id': None
    }
    all_id = db.get_all_id()
    while True:
        unique_id = str(message.from_user.id) + "_" + str(randint(0, 999))
        if unique_id in all_id:
            continue
        else:
            user_data[message.chat.id]['unique_id'] = unique_id
            break
    msg = bot.send_message(
        message.chat.id,
        "Введите сколько вопросов будет в тесте:\n\n"
        "Пример: 10"
    )
    bot.register_next_step_handler(msg, check_count)


def check_count(message):
    try:
        count = int(message.text)
        user_data[message.chat.id]['count'] = count
        data = user_data[message.chat.id]
        db.add_test(data['name'], data['unique_id'])
        question(message.chat.id)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Это не число, попробуйте еще раз:\n\n"
            "Пример: 10"
        )
        bot.register_next_step_handler(message, check_count)


def question(chat_id):

    msg = bot.send_message(
        chat_id,
        f"Введите {user_data[chat_id]['questions_done'] + 1}-ый вопрос:"
    )
    bot.register_next_step_handler(msg, question_text)


def question_text(message):
    user_data[message.chat.id]['current_question'] = message.text

    msg = bot.send_message(
        message.chat.id,
        'Введите варианты ответа через запятую: \n\n'
        'Пример: Хлеб, Вода, Спирт, Химия'
    )

    bot.register_next_step_handler(msg, get_answers)


def get_answers(message):
    answers = message.text
    msg = bot.send_message(
        message.chat.id,
        'Введите номер правильного ответа:\n\n'
        'Пример: 1'
    )
    bot.register_next_step_handler(msg, check_correct_answer, answers)


def check_correct_answer(message, answers):
    try:
        correct = int(message.text)
        finish_question(message, answers, correct)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Это не число, попробуйте еще раз:\n\n"
            "Пример: 1"
        )
        bot.register_next_step_handler(message, check_correct_answer, answers)


def finish_question(message, answers, correct):
    chat_id = message.chat.id
    data = user_data[chat_id]

    db.add_question(data['current_question'], answers, correct, data['unique_id'])

    data['questions_done'] += 1

    if data['questions_done'] < data['count']:
        question(chat_id)
    else:
        bot.send_message(
            chat_id,
            'Тест успешно создан!\n'
            f'Ваша ссылка: https://t.me/forlessons_coursebot?start={data['unique_id']}')
        del user_data[chat_id]


@bot.message_handler(func=lambda message: message.text == 'Delete Test 🗑')
def delete_test_handler(message):
    tests = db.get_user_tests(message.from_user.id)

    if tests:
        response = ("Введите номер теста для удаления:\n\n"
                    "Пример: 1\n\n")
        for i, (title, unique_id) in enumerate(tests):
            response += f"{i + 1}. {title}\n"
        bot.send_message(message.chat.id, response)
        bot.register_next_step_handler(message, confirm_delete, tests)
    else:
        bot.send_message(message.chat.id, "У вас нет тестов")


def confirm_delete(message, tests):
    try:
        num = int(message.text) - 1
        if num < 0 or num >= len(tests):
            bot.send_message(message.chat.id, "Неверный номер, введите еще раз: ")
            bot.register_next_step_handler(message, confirm_delete, tests)
            return
        title, unique_id = tests[num]
        db.delete_test(unique_id)
        bot.send_message(message.chat.id, f"Тест '{title}' удалён")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный номер, введите еще раз: ")
        bot.register_next_step_handler(message, confirm_delete, tests)


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(
        message.chat.id,
        f"Такой функции нету, нажми старт чтобы перезапустить /start"
    )



bot.infinity_polling()
