from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """Функция для безопасного подключения к PostgreSQL"""
    retries = 5
    while retries > 0:
        try:
            # sslmode='require' обязателен для работы с Neon.tech
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            return conn
        except Exception as e:
            print(f"Ошибка подключения: {e}. Повтор через 2 сек...")
            retries -= 1
            time.sleep(2)
    raise Exception("Не удалось подключиться к облачной базе данных")

def init_db():
    """Создание таблицы пользователей с уникальными полями"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

try:
    if DATABASE_URL:
        init_db()
except Exception as e:
    print(f"Ошибка инициализации БД: {e}")

@app.get("/")
async def home():
    return {"status": "online", "message": "FastAPI + PostgreSQL is working!"}

@app.post("/users")
async def add_user(request: Request):
    """Регистрация пользователя с проверкой на дубликаты"""
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Некорректный JSON")

    u = str(data.get("username", "")).strip()
    p = str(data.get("password", "")).strip()
    e = str(data.get("email", "")).strip()

    if not u or not p or not e:
        raise HTTPException(status_code=400, detail="Заполните все поля!")
    if len(p) < 6:
        raise HTTPException(status_code=400, detail="Минимум 6 символов!")  
    if "@" not in e or "." not in e:
        raise HTTPException(status_code=400, detail="Неправильный емейл!")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
            (u, p, e)
        )
        conn.commit()
        return {"status": "success", "message": "Пользователь успешно создан"}
    
    except psycopg2.errors.UniqueViolation as err:
        conn.rollback()
        error_msg = str(err).lower()
        if "username" in error_msg:
            raise HTTPException(status_code=400, detail="Это имя пользователя уже занято")
        elif "email" in error_msg:
            raise HTTPException(status_code=400, detail="Эта почта уже зарегистрирована")
        else:
            raise HTTPException(status_code=400, detail="Такие данные уже существуют")
            
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()

@app.get("/users")
async def get_users():
    """Получение списка пользователей"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT username, email FROM users")
        users = cursor.fetchall()
        return {"status": "success", "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)