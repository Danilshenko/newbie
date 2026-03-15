from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
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

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, email FROM users')
        users = cursor.fetchall()
        conn.close()
        
        user_list = []
        for u in users:
            user_list.append({
                "username": u[0],
                "password": u[1],
                "email": u[2]
            })
        return jsonify({"status": "success", "data": user_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    # Получаем JSON данные из запроса
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({"status": "error", "message": "Данные не получены или не являются JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"status": "error", "message": "Заполните все поля: username, password, email"}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (str(username), str(password), str(email)))
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": f"Пользователь {username} успешно сохранен!"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка базы данных: {str(e)}"}), 500

@app.route('/user/<name>')
def get_user_profile(name):
    try:
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
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)