from flask import Flask, request, jsonify, render_template
import sqlite3
from threading import Lock

app = Flask(__name__) # Создаем экзмепляр приложения Фласк

# Подключение к БД
db_path = 'application.db'
db_lock = Lock()
# Функция для получения пдключения к базе данных
def get_db_connection():
    with db_lock:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST']) # Декоратор для маршрута 
def submit_application(): #Получаем данные из формы
    conn, cursor = get_db_connection()
    name = request.form.get('name')
    email = request.form.get ('email')
    message = request.form.get ('message')
    attachment = request.files.getlist('attachments')[0] #Получить вложение
 
    cursor.execute("""
    INSERT INTO application (name, email, message, attachment_filename) VALUES (?, ?, ?, ?);""", 
    (name, email, message, attachment.filename))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify ({"status": "success"}), 200

if __name__ == '__main__':
    # Создание таблицы "applications" (если она не сущесвтует)
    conn, cursor = get_db_connection()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    attachment_filename TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    app.run(debug=True, port=80)