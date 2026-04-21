from all_db import Database

db = Database()

def show_my_tests(bot, message):
    user_id = message.from_user.id
    tests = db.get_user_tests(user_id)
    
    if tests:
        response = "Ваши тесты:\n\n"
        for test in tests:
            title = test[0]
            unique_id = test[1]
            response += f"📋 {title}\n"
            response += f"https://t.me/forlessons_coursebot?start={unique_id}"
        bot.send_message(
            message.chat.id,
            response,
        )
    else:
        bot.send_message(message.chat.id, "Нет созданных тестов")
