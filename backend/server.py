from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
   
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        return jsonify({"status": "error", "message": "Заполните все поля"}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password , email) VALUES (?, ?, ?)', 
                       (username, password, email))
        conn.commit()
        return jsonify({"status": "success", "message": f"Пользователь {username} сохранен!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

@app.route('/user/<name>')
def get_user_profile(name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT username, password, email FROM users WHERE username = ?', (name,))
    
    user = cursor.fetchone()
    conn.close()

    if user:
        #кортеж
        return jsonify({
            "status": "success",
            "data": {
                "username": user[0],
                "password": user[1],
                "email": user[2]
            }
        })
    else:
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 404

if __name__ == '__main__':
    init_db()  
    app.run(debug=True,host='0.0.0.0', port=5000)