from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.conf.config import settings

async def send_verification_email(to_email: str, token: str):
    """
    Send a verification email to the user.
    """
    subject = "Email Verification"
    body = f"Please verify your email by clicking this link: http://localhost:8000/api/auth/verify/{token}"
    await send_email(to_email, subject, body)

async def send_email(to_email: str, subject: str, body: str):
    """
    Send an email using FastMail.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="html"
    )
    
    config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        SUPPRESS_SEND=settings.TESTING  # Suppress sending emails during testing
    )
    
    fm = FastMail(config)
    await fm.send_message(message) 