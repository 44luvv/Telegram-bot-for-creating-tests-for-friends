from urllib3 import request

from all_db import Database

func = Database()

def start_test(bot, message, unique_id):
    title = func.get_test_by_id(unique_id)

    if title:
        bot.send_message(
            message.chat.id,
            f"Вы начали тест: {title}\n"
        )
        answer_question(message, bot, unique_id, 0, 0)
    else:
        bot.send_message(
            message.chat.id,
            "Тест не найден или ссылка недействительна! "
        )


def answer_question(message, bot, unique_id, i, count_of_correct):
    text = func.get_question(unique_id)
    answer = func.get_answer(unique_id)
    correct = func.get_correct_answer(unique_id)

    var = answer[i].split(',')

    bot.send_message(
        message.chat.id,
        f'{i + 1}-ый вопрос: {text[i]}\n'
        f'Введите номер ответа (Пример: 1): '
    )
    msg = ''
    for j in range(len(var)):
        msg += f"{j + 1} - {var[j]}\n"

    bot.send_message(
        message.chat.id,
        msg
    )

    bot.register_next_step_handler(message, is_correct, bot, unique_id, text, i, count_of_correct, correct)


def is_correct(message, bot, unique_id, text, i, count_of_correct, correct):
    if str(correct[i]) == message.text:
        bot.send_message(
            message.chat.id,
            "Correct!\n"
        )
        count_of_correct += 1
    else:
        bot.send_message(
            message.chat.id,
            f"Incorrect answer!\n"
        )

    if i == len(text) - 1:
        title = func.get_test_by_id(unique_id)
        chat_id = unique_id.split('_')[0]
        bot.send_message(
            chat_id,
            f"Пользователь {message.from_user.username} прошел ваш тест {title}\n"
            f"Правильных ответов: {count_of_correct}"
        )
        return

    i += 1
    answer_question(message, bot, unique_id, i, count_of_correct)
