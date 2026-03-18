from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time
import jwt
from datetime import datetime, timedelta
import json

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-123")
ALGORITHM = "HS256"
DATABASE_URL = os.environ.get("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    """Подключение к базе (теперь оно работает, а не pass)"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except Exception as e:
        print(f"Ошибка базы: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к БД")


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/")
async def home():
    return {"status": "online", "message": "Backend is running"}


@app.post("/users")
async def add_user(request: Request):
    """Регистрация: теперь данные реально сохраняются"""
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
        raise HTTPException(status_code=400, detail="Пароль слишком короткий!")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (u, p, e),
        )
        conn.commit()
        return {"status": "success", "message": "Пользователь создан"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Логин или почта уже заняты")
    finally:
        cursor.close()
        conn.close()


@app.post("/login")
async def login(request: Request):
    """Вход и выдача токена"""
    data = await request.json()
    u = data.get("email")
    p = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (u,))
        user = cursor.fetchone()

        if not user or user["password"] != p:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        token = create_access_token(u)
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()


@app.get("/users")
async def get_users():
    """Проверка списка пользователей"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT username, email FROM users")
        users = cursor.fetchall()
        return {"data": users}
    finally:
        cursor.close()
        conn.close()


@app.post("/click")
async def add_click(request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Токен хуевый или отсутствует")

    conn = None

    try:

        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT basket FROM users WHERE email = %s", (user_email,))
        result = cursor.fetchone()

        basket = result["basket"] if result and result["basket"] is not None else []

        new_event = {"action": "click", "time": datetime.now().isoformat()}
        basket.append(new_event)

        cursor.execute(
            "UPDATE users SET basket = %s WHERE email = %s",
            (json.dumps(basket), user_email),
        )
        conn.commit()
        cursor.close()

        return {"status": "success", "current_basket": basket}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="нету такого токена")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Ошибка сервера: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка Базы: {str(e)}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
