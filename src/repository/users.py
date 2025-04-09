from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserCreate
from src.services.auth import hash_password


def create_user(db: Session, user_data: UserCreate):
    """
        Create a new user in the database.

        This function checks if a user with the given email already exists. If not,
        it hashes the user's password, creates a new user record, and saves it to the database.

        Args:
            db (Session): The database session.
            user_data (UserCreate): The user data for creating a new user.

        Returns:
            User: The created user object, or None if a user with the same email already exists.
        """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password, is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str):
    """
        Retrieve a user by their email address.

        Args:
            db (Session): The database session.
            email (str): The email of the user to fetch.

        Returns:
            User: The user object, or None if no user with the given email exists.
        """
    return db.query(User).filter(User.email == email).first()


def verify_user_email(db: Session, email: str):
    """
        Verify the email of a user by setting the `is_verified` flag to True.

        Args:
            db (Session): The database session.
            email (str): The email of the user to verify.

        Returns:
            User: The user object with the updated verification status.
        """
    user = db.query(User).filter(User.email == email).first()
    if user and not user.is_verified:
        user.is_verified = True
        db.commit()
        db.refresh(user)
    return user
