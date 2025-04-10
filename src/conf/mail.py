from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv
from src.services.email import send_email

load_dotenv()

class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Rest API Service",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_verification_email(email: str, token: str):
    """
    Send a verification email to the user.
    """
    subject = "Verify your email"
    body = f"""
    <html>
        <body>
            <h1>Welcome to Contact Management System!</h1>
            <p>Please click the link below to verify your email address:</p>
            <p><a href="http://localhost:8000/api/auth/verify/{token}">Verify Email</a></p>
            <p>If you did not create an account, please ignore this email.</p>
        </body>
    </html>
    """
    await send_email(email, subject, body)
