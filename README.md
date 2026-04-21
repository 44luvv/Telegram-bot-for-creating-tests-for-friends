<div align="center">

# 📋 CourseBot

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/pyTelegramBotAPI-4.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/status-active-success?style=for-the-badge"/>

<br/>

> Telegram бот для создания и прохождения тестов. Создавай тесты, делись ссылками с друзьями и смотри результаты.

</div>

---

## ✨ Возможности

- 📝 **Создание тестов** — задавай вопросы с вариантами ответов
- 🔗 **Уникальная ссылка** — каждый тест получает свою ссылку для прохождения
- ✅ **Прохождение теста** — пользователи проходят тест по ссылке
- 📊 **Результаты** — создатель теста получает уведомление с результатами
- 🗂 **Мои тесты** — список всех созданных тестов со ссылками
- 🗑 **Удаление тестов** — удаляй ненужные тесты

---

## 🚀 Запуск

### 1. Клонируй репозиторий
```bash
git clone https://github.com/your/repo.git
cd repo
```

### 2. Установи зависимости
```bash
pip install -r requirements.txt
```

### 3. Настрой `.env` файл
Переименуй `.env.example` в `.env` и вставь свои данные:
```env
BOT_TOKEN=your_bot_token
DBNAME=your_db_name
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432
```

### 4. Запусти бота
```bash
python main.py
```

---

## 🗂 Структура проекта

```
📦 CourseBot
 ┣ 📜 main.py       — основной файл, хэндлеры бота
 ┣ 📜 test.py       — логика прохождения теста
 ┣ 📜 list.py       — вывод списка тестов пользователя
 ┣ 📜 all_db.py     — работа с базой данных
 ┗ 📜 .env          — переменные окружения
```

---

## 🗃 База данных

```
tests
 ┣ id
 ┣ title
 ┗ unique_id

questions
 ┣ id
 ┣ unique_id
 ┗ question_text

answers
 ┣ id
 ┣ unique_id
 ┣ answer_text
 ┗ correct_answer
```

---

## 📖 Как пользоваться

### Создание теста
1. Нажми **Create Test 📋**
2. Введи название теста
3. Укажи количество вопросов
4. Для каждого вопроса введи:
   - Текст вопроса
   - Варианты ответов через запятую
   - Номер правильного ответа
5. Получи ссылку на тест 🎉

### Прохождение теста
1. Перейди по ссылке `/start unique_id`
2. Отвечай на вопросы вводя номер ответа
3. Создатель теста получит результаты

---

<div align="center">

Made with ❤️ and Python

</div>
