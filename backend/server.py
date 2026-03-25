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


SENDER_EMAIL = "1509zii2008@gmail.com"
SENDER_PASSWORD = "ycno tmuz zhsz ixbq"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-123")
ALGORITHM = "HS256"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@host:5432/dbname")

app = FastAPI(redirect_slashes=True)

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
        print(f"Ошибка подключения к БД: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к БД")

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                basket JSONB DEFAULT '[]',
                verification_code TEXT,
                is_active BOOLEAN DEFAULT FALSE
            );
        """)
        conn.commit()
        print(" База данных готова")
    except Exception as e:
        print(f" Ошибка инициализации базы: {e}")
    finally:
        if conn:
            conn.close()

init_db()

# --- УТИЛИТЫ ---
def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/")
async def home():
    return {"status": "online", "message": "Backend is running"}

@app.post("/users")
async def add_user(request: Request):
    try:
        data = await request.json()
        u = str(data.get("username", "")).strip()
        p = str(data.get("password", "")).strip()
        e = str(data.get("email", "")).strip()

        if not u or not p or not e:
            raise HTTPException(status_code=400, detail="Заполните все поля!")

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
            conn.rollback()
            print(f"Ошибка при регистрации: {err}")
            raise HTTPException(status_code=400, detail=f"Ошибка: {str(err)}")
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=400, detail="Некорректный запрос")

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or user["password"] != password:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        if not user.get("is_active"):
            return {
                "status": "pending_verification",
                "message": "Подтвердите почту",
                "email": email
            }

        token = create_access_token(email)
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()

@app.post("/verify-email")
async def verify_email(request: Request):
    data = await request.json()
    email = data.get("email")
    code = str(data.get("code"))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND verification_code = %s",
            (email, code),
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=400, detail="Неверный код")

        cursor.execute(
            "UPDATE users SET is_active = TRUE, verification_code = NULL WHERE email = %s",
            (email,),
        )
        conn.commit()


        token = create_access_token(email)
        return {
            "status": "success",
            "message": "Почта подтверждена!",
            "access_token": token,
            "token_type": "bearer"
        }
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
