from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from src.conf.config import settings

conf = ConnectionConfig(
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

async def send_verification_email(to_email: str, token: str, base_url: str):
    """
    Send a verification email to the user.
    
    Args:
        to_email: str - The recipient's email address
        token: str - The verification token
        base_url: str - The base URL of the application
    """
    subject = "Email Verification"
    verification_link = f"{base_url}/api/auth/verify/{token}"
    body = f"""
    <html>
        <body>
            <h1>Email Verification</h1>
            <p>Please verify your email by clicking the link below:</p>
            <p><a href="{verification_link}">Verify Email</a></p>
            <p>If you did not request this verification, please ignore this email.</p>
            <p>Best regards,<br>Your Application Team</p>
        </body>
    </html>
    """
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
    
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_password_reset_email(email: EmailStr, token: str, base_url: str):
    """
    Send a password reset email to the user.
    
    Args:
        email: EmailStr - The recipient's email address
        token: str - The password reset token
        base_url: str - The base URL of the application
    """
    reset_link = f"{base_url}/reset-password?token={token}"
    
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>You have requested to reset your password. Click the link below to proceed:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>If you did not request this password reset, please ignore this email.</p>
                <p>This link will expire in 1 hour.</p>
                <p>Best regards,<br>Your Application Team</p>
            </body>
        </html>
        """,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message) 