from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def home():
    return {
        "status": "success",
        "message": "FastAPI backend is running!",
        "endpoints": {
            "all_users": "/users (GET)",
            "register": "/users (POST)",
            "profile": "/user/{name} (GET)"
        }
    }

@app.get("/users")
async def get_users():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, email FROM users")
        users = cursor.fetchall()
        conn.close()

        return {
            "status": "success", 
            "data": [{"username": u[0], "password": u[1], "email": u[2]} for u in users]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users")
async def add_user(request: Request):
    data = await request.json()
    
    u = str(data.get("username", "")).strip()
    p = str(data.get("password", "")).strip()
    e = str(data.get("email", "")).strip()

    if not u or not p or not e:
        raise HTTPException(status_code=400, detail="Все поля должны быть заполнены")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (u, p, e)
        )
        conn.commit()
        return {"status": "success", "message": f"Пользователь {u} сохранен"}, 201
    except sqlite3.IntegrityError as err:
        error_msg = str(err).lower()
        if "username" in error_msg:
            raise HTTPException(status_code=400, detail="это мой гриб я его ем!!")
        elif "email" in error_msg:
            raise HTTPException(status_code=400, detail="пидор ты ебаный!!")
        else:
            raise HTTPException(status_code=400, detail="Данные уже существуют")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        conn.close()

@app.get("/user/{name}")
async def get_user_profile(name: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, email FROM users WHERE username = ?", (name,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "status": "success",
            "data": {"username": user[0], "password": user[1], "email": user[2]}
        }
    raise HTTPException(status_code=404, detail="Пользователь не найден")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
