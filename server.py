from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import jwt
from datetime import datetime, timedelta
import json
import random
import httpx

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY", "your-super-secret-key")
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


async def send_verification_email(email: str, code: str):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": "Код подтверждения",
        "html": f"<p>Ваш код для входа: <strong>{code}</strong></p>",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.status_code == 200 or response.status_code == 201


def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/users")
async def register(request: Request):
    data = await request.json()
    u, p, e = data.get("username"), data.get("password"), data.get("email")

    if not all([u, p, e]):
        raise HTTPException(status_code=400, detail="Заполните все поля")

    code = str(random.randint(1000, 9999))

    email_success = await send_verification_email(e, code)
    if not email_success:
        raise HTTPException(status_code=500, detail="Ошибка отправки письма через API")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email, verification_code, is_active) VALUES (%s, %s, %s, %s, FALSE)",
            (u, p, e, code),
        )
        conn.commit()
        return {"status": "success", "message": "Код отправлен"}
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    finally:
        cursor.close()
        conn.close()


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    e, p = data.get("email"), data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (e, p))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Неверные данные")

    if not user["is_active"]:
        return {"status": "pending_verification", "message": "Нужно подтверждение"}

    return {"status": "success", "access_token": create_access_token(e)}


@app.post("/verify-email")
async def verify(request: Request):
    data = await request.json()
    e, c = data.get("email"), str(data.get("code"))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND verification_code = %s", (e, c)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=400, detail="Неверный код")
    cursor.execute(
        "UPDATE users SET is_active = TRUE, verification_code = NULL WHERE email = %s",
        (e,),
    )
    conn.commit()
    conn.close()

    return {"status": "success", "access_token": create_access_token(e)}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
