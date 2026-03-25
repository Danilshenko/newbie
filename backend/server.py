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
DATABASE_URL = os.environ.get("DATABASE_URL") 

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
        print(f"CRITICAL: Ошибка подключения к БД: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

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
        print("✅ Таблица пользователей проверена/создана")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
    finally:
        if conn: conn.close()

init_db()

def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/")
async def home():
    return {"status": "online", "message": "Backend is running on Render"}

@app.post("/users")
async def register(request: Request):
    try:
        data = await request.json()
        u = str(data.get("username", "")).strip()
        p = str(data.get("password", "")).strip()
        e = str(data.get("email", "")).strip()

        if not u or not p or not e:
            raise HTTPException(status_code=400, detail="Заполните все поля")

        code = str(random.randint(1000, 9999))
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            msg = EmailMessage()
            msg.set_content(f"Ваш код подтверждения: {code}")
            msg["Subject"] = "Код подтверждения"
            msg["From"] = SENDER_EMAIL
            msg["To"] = e

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls() 
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)

            cursor.execute(
                "INSERT INTO users (username, password, email, verification_code, is_active) VALUES (%s, %s, %s, %s, FALSE)",
                (u, p, e, code),
            )
            conn.commit()
            return {"status": "success", "message": "Код отправлен на email"}

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Email или логин уже заняты")
        except Exception as err:
            conn.rollback()
            print(f"ОШИБКА СЕТИ ИЛИ ПОЧТЫ: {err}")
            raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(err)}")
        finally:
            cursor.close()
            conn.close()
    except Exception as main_err:
        if isinstance(main_err, HTTPException): raise main_err
        raise HTTPException(status_code=400, detail="Неверные данные")

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
            raise HTTPException(status_code=401, detail="Неверные данные входа")

        if not user["is_active"]:
            return {
                "status": "pending_verification",
                "message": "Нужно подтвердить почту",
                "email": email
            }

        token = create_access_token(email)
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()

@app.post("/verify-email")
async def verify(request: Request):
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
            "access_token": token,
            "token_type": "bearer",
            "message": "Почта подтверждена!"
        }
    finally:
        cursor.close()
        conn.close()

@app.get("/me")
async def get_me(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401)
    
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT username, email, basket FROM users WHERE email = %s", (email,))
        return {"status": "success", "data": cursor.fetchone()}
    except:
        raise HTTPException(status_code=401, detail="Токен истек или неверен")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)