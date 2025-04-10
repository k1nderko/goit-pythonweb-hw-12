import asyncio
from unittest.mock import AsyncMock, patch
from contextlib import contextmanager

async def mock_send_verification_email(email: str, token: str):
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
    Context manager that patches both verification and regular email services.
    Usage:
        with patch_email_service():
            # Run tests that need email functionality
    """
    with patch('src.conf.mail.send_verification_email', mock_send_verification_email), \
         patch('src.services.email.send_email', mock_send_email):
        yield 