from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Создаем таблицу с полями id, username, password и email
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 1. Главная страница
@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Backend is running!",
        "endpoints": {
            "all_users": "/users (GET)",
            "register": "/users (POST)",
            "profile": "/user/<name> (GET)"
        }
    })

# 2. Получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, email FROM users')
    users = cursor.fetchall()
    conn.close()
    
    user_list = [{"username": u[0], "password": u[1], "email": u[2]} for u in users]
    return jsonify({"status": "success", "data": user_list})

# 3. Регистрация нового пользователя
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"status": "error", "message": "Fill all fields: username, password, email"}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (username, password, email))
        conn.commit()
        return jsonify({"status": "success", "message": f"User {username} saved!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# 4. Профиль конкретного пользователя
@app.route('/user/<name>')
def get_user_profile(name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, email FROM users WHERE username = ?', (name,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "data": {
                "username": user[0],
                "password": user[1],
                "email": user[2]
            }
        })
    return jsonify({"status": "error", "message": "User not found"}), 404

# Блок запуска
if __name__ == '__main__':
    init_db()
    # Используем порт из переменной окружения для Render или 5000 для локалки
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)