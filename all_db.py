import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
        )

    def init_db(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tests (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    unique_id TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    unique_id TEXT NOT NULL,
                    question_text TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS answers (
                    id SERIAL PRIMARY KEY,
                    unique_id TEXT NOT NULL,
                    answer_text TEXT NOT NULL,
                    correct_answer INTEGER NOT NULL
                );
            """)

            self.connection.commit()

    def add_test(self, title, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO tests (title, unique_id) VALUES (%s, %s);",
                (title, unique_id)
            )
            self.connection.commit()

    def add_question(self, question, answer, correct, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO questions (unique_id, question_text) VALUES (%s, %s);",
                (unique_id, question)
            )

            cur.execute(
                "INSERT INTO answers (unique_id, answer_text, correct_answer) VALUES (%s, %s, %s);",
                (unique_id, answer, correct)
            )
            self.connection.commit()

    def get_test_by_id(self, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                'SELECT title FROM tests WHERE unique_id = (%s)',
                (unique_id,))
            title = cur.fetchone()
            return title[0] if title else None

    def get_question(self, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                'SELECT question_text FROM questions WHERE unique_id = %s',
                (unique_id,))
            question = cur.fetchall()
            return [q[0] for q in question] if question else None

    def get_answer(self, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                'SELECT answer_text FROM answers WHERE unique_id = %s',
                (unique_id,))
            answer = cur.fetchall()
            return [a[0] for a in answer] if answer else None

    def get_correct_answer(self, unique_id):
        with self.connection.cursor() as cur:
            cur.execute(
                'SELECT correct_answer FROM answers WHERE unique_id = %s',
                (unique_id,))
            correct = cur.fetchall()
            return [c[0] for c in correct] if correct else None

    def get_user_tests(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute(
                'SELECT title, unique_id FROM tests WHERE unique_id LIKE %s',
                (f'{user_id}_%',))
            tests = cur.fetchall()
            return tests if tests else None


    def get_all_id(self):
        with self.connection.cursor() as cur:
            cur.execute('SELECT unique_id FROM tests')
            ids = cur.fetchall()
            return [i[0] for i in ids] if ids else []

    def delete_test(self, unique_id):
        with self.connection.cursor() as cur:
            cur.execute('DELETE FROM tests WHERE unique_id = %s', (unique_id,))
            cur.execute('DELETE FROM questions WHERE unique_id = %s', (unique_id,))
            cur.execute('DELETE FROM answers WHERE unique_id = %s', (unique_id,))
            self.connection.commit()
