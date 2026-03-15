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
                "username": str(u[0]),
                "password": str(u[1]),
                "email": str(u[2])
            })
        return jsonify({"status": "success", "data": user_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json(force=True, silent=True)
    except:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    if not data or not isinstance(data, dict):
        return jsonify({"status": "error", "message": "JSON required"}), 400

    u_val = data.get('username')
    p_val = data.get('password')
    e_val = data.get('email')

    if u_val is None or p_val is None or e_val is None:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    username = str(u_val)
    password = str(p_val)
    email = str(e_val)

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (username, password, email))
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": f"User {username} saved"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/user/<name>')
def get_user_profile(name):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, email FROM users WHERE username = ?', (str(name),))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "status": "success",
                "data": {
                    "username": str(user[0]),
                    "password": str(user[1]),
                    "email": str(user[2])
                }
            })
        return jsonify({"status": "error", "message": "Not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)