from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import jwt
from datetime import datetime, timedelta
import json
import random
import smtplib
from email.message import EmailMessage


def init_db():
    """Эта функция создаст таблицу автоматически при запуске сервера"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                basket JSONB DEFAULT '[]',
                verification_code TEXT,
                is_active BOOLEAN DEFAULT FALSE
            );
        """
        )
        conn.commit()
        print(" База данных проверена и готова к работе")
    except Exception as e:
        print(f" Ошибка инициализации базы: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


init_db()

SENDER_EMAIL = "1509zii2008@gmail.com"
SENDER_PASSWORD = "ycno tmuz zhsz ixbq"

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-123")
ALGORITHM = "HS256"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@host:5432/dbname")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except Exception as e:
        print(f"Ошибка базы: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к БД")


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/")
async def home():
    return {"status": "online", "message": "Backend is running"}

@app.post("/users")
async def add_user(request: Request):
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

    verification_code = str(random.randint(1000, 9999))
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        msg = EmailMessage()
        msg.set_content(f"Ваш код подтверждения: {verification_code}")
        msg["Subject"] = "Код подтверждения"
        msg["From"] = SENDER_EMAIL
        msg["To"] = e

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        cursor.execute(
            "INSERT INTO users (username, password, email, verification_code, is_active) VALUES (%s, %s, %s, %s, FALSE)",
            (u, p, e, verification_code),
        )
        conn.commit()
        return {"status": "success", "message": "Код отправлен на почту!"}

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Логин или почта уже заняты")
    except Exception as err:
        if conn:
            conn.rollback()
        print(f"Ошибка: {err}")
        raise HTTPException(status_code=400, detail="Ошибка при регистрации")
    finally:
        cursor.close()
        conn.close()


@app.post("/verify-email")
async def verify_email(request: Request):
    data = await request.json()
    email = data.get("email")
    code = data.get("code")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND verification_code = %s",
            (email, str(code)),
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=400, detail="Неверный код")

        cursor.execute(
            "UPDATE users SET is_active = TRUE, verification_code = NULL WHERE email = %s",
            (email,),
        )
        conn.commit()
        return {"status": "success", "message": "Почта подтверждена!"}
    finally:
        cursor.close()
        conn.close()


@app.post("/login")
async def login(request: Request):
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

        if not user.get("is_active"):
            raise HTTPException(status_code=403, detail="Подтвердите почту!")

        token = create_access_token(u)
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()


@app.post("/favorites")
async def toggle_favorite(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Авторизуйтесь")

    try:
        item_data = await request.json()
        product_id = item_data.get("id")
    except:
        raise HTTPException(status_code=400, detail="Некорректные данные")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        cursor.execute("SELECT basket FROM users WHERE email = %s", (user_email,))
        result = cursor.fetchone()

        basket = result["basket"] if result and result["basket"] else []
        if isinstance(basket, str):
            basket = json.loads(basket)

        existing = next((i for i in basket if i.get("id") == product_id), None)
        if existing:
            basket = [i for i in basket if i.get("id") != product_id]
            msg = "Удалено"
        else:
            item_data["added_at"] = datetime.now().isoformat()
            basket.append(item_data)
            msg = "Добавлено"

        cursor.execute(
            "UPDATE users SET basket = %s WHERE email = %s",
            (json.dumps(basket), user_email),
        )
        conn.commit()
        return {"status": "success", "message": msg, "favorites": basket}
    finally:
        cursor.close()
        conn.close()


@app.get("/me")
async def get_me(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401)

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        cursor.execute(
            "SELECT username, email, basket FROM users WHERE email = %s", (user_email,)
        )
        user_data = cursor.fetchone()
        return {"status": "success", "data": user_data}
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10000)
