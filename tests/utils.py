import asyncio
from unittest.mock import AsyncMock, patch
from contextlib import contextmanager
from fastapi_mail import ConnectionConfig

async def mock_send_verification_email(email: str, token: str, base_url: str):
    """
    Mock function for sending verification emails.
    """
    # Simulate a small delay to mimic real email sending
    await asyncio.sleep(0.1)
    return True

async def mock_send_email(to_email: str, subject: str, body: str):
    """
    Mock function for sending regular emails.
    """
    # Simulate a small delay to mimic real email sending
    await asyncio.sleep(0.1)
    return True

@contextmanager
def patch_email_service():
    """
    Context manager that patches the email service.
    Usage:
        with patch_email_service():
            # Run tests that need email functionality
    """
    with patch.multiple(
        'src.services.email',
        send_verification_email=AsyncMock(return_value=True),
        send_email=AsyncMock(return_value=True),
        send_password_reset_email=AsyncMock(return_value=True)
    ):
        yield 