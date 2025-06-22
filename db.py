import sqlite3
import queries
from typing import List
import bcrypt

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False) or None
        if self.conn is None:
            print("Error: Could not connect to the database")
            return

    def get_answer_by_quiz_id(self, quiz_id):
        cursor = self.conn.cursor()
        query = "SELECT question_id, correct_ans FROM questions WHERE quiz_id = ?"
        cursor.execute(query, tuple(quiz_id,))
        return cursor.fetchall()

    def insert_samples(self):
        cursor = self.conn.cursor()

        quizzes = [
            ("Programming", "Test your coding skills with questions on Python, Java, and more."),
            ("Mathematics", "Challenge yourself with algebra, geometry, and calculus."),
            ("Science", "Explore physics, chemistry, and biology concepts.")
        ]
        cursor.executemany("INSERT OR IGNORE INTO quizzes (title, description) VALUES (?, ?)", quizzes)
        print("Info: Sample quizzes inserted")

        questions = [
            (1, "In a language where variables declared inside functions are function-scoped, not block-scoped, imagine a loop runs several times and creates multiple closures that all use the same loop variable. After the loop ends, all the closures are executed. What will each closure output?",
            "A sequence of increasing numbers", "The same final value, repeated", "Random values depending on memory state", "An error due to variable reuse", "The same final value, repeated"),
            (1, "Which of the following is NOT a condition for deadlock in a concurrent system?",
            "Mutual exclusion", "Hold and wait", "Preemption", "Circular wait", "Preemption"),
            (1, "Which algorithm can be used to find the shortest path in a graph with negative edge weights, assuming no negative cycles?",
            "Dijkstra’s Algorithm", "Bellman-Ford Algorithm", "Floyd-Warshall Algorithm", "Kruskal’s Algorithm", "Bellman-Ford Algorithm"),
            (2, "How many 5-digit numbers can be formed using the digits 1–9 without repetition and such that the number is odd?",
            "8400", "15,120", "20,160", "30,240", "8400"),
            (2, "Given 𝑓(𝑥+𝑦)+𝑓(𝑥−𝑦)=2𝑓(𝑥)𝑓(𝑦), which of the following is a valid solution?",
            "𝑓(𝑥) = 𝑥", "𝑓(𝑥) = cos(𝑥)", "𝑓(𝑥) = cosh(𝑥)", "𝑓(𝑥) = cos(𝑎𝑥) for some constant 𝑎", "𝑓(𝑥) = cos(𝑎𝑥) for some constant 𝑎"),
            (2, "What is the value of (1+i)^8, where 𝑖 is the imaginary unit?",
            "0", "16i", "-16", "16", "16"),
            (3, "What is the pH of a 0.001 M HCl solution?",
            "1", "2", "3", "4", "3"),
            (3, "Which of the following enzymes removes RNA primers during DNA replication in eukaryotes?",
            "DNA polymerase III", "Helicase", "DNA polymerase I", "RNase H", "RNase H"),
            (3, "Which of the following cannot be precisely known at the same time, according to the Heisenberg Uncertainty Principle?",
            "Mass and charge", "Position and momentum", "Energy and wavelength", "Speed and acceleration", "Position and momentum")
        ]
        cursor.executemany(
            '''
                INSERT OR IGNORE INTO questions (
                    quiz_id,
                    question_text,
                    option1,
                    option2,
                    option3,
                    option4,
                    correct_ans
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', questions
        )
        print("Info: Sample questions inserted")

        cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("a", "aaaaaaaaaaaaaaaaaaaa"))
        print("Info: Sample users inserted")

        self.conn.commit()

    def create_table(self, tb_name):
        cursor = self.conn.cursor()

        if tb_name == "quizzes":
            cursor.execute(queries.CREATE_QUIZ_TABLE)
        elif tb_name == "questions":
            cursor.execute(queries.CREATE_QUESTIONS_TABLE)
        elif tb_name == "users":
            cursor.execute(queries.CREATE_USERS_TABLE)
        elif tb_name == "attempts":
            cursor.execute(queries.CREATE_ATTEMPTS_TABLE)

    def close_connection(self):
        self.conn.close()

    def get_quizzes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quizzes")
        quizzes = cursor.fetchall()
        return quizzes

    def get_questions(self, quiz_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
        questions = cursor.fetchall()
        return questions

    def get_title(self, quiz_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT title FROM quizzes WHERE quiz_id = ?", (quiz_id,))
        title = cursor.fetchall()
        return title[0][0]

    def fetch_user(self, username, password):
        cursor = self.conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = (?)", (username,)).fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), hashed_password=user[2]):
            return user
        return None

    def create_user(self, username, password):
        cursor = self.conn.cursor()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        self.conn.commit()

    def save_attempt(self, user_id, quiz_id, question_id, selected_answer, score):
        cursor = self.conn.cursor()
        cursor.execute(queries.CREATE_USER_ATTEMPT, (user_id, quiz_id, question_id, selected_answer, score))
        self.conn.commit()
    
    def get_user_attempts(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(queries.GET_USER_ATTEMPTS, (user_id,))
        return cursor.fetchall()
        
db = Database("quiz.db")
if __name__ == "__main__":
    db.create_table("quizzes")
    db.create_table("questions")
    db.create_table("users")
    db.create_table("attempts")
    db.insert_samples()