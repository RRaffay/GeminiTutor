from firebase_admin import auth
from .init import db
from .database import create_user_document
from app.auth.models import User


def create_user(email, password, first_name, last_name, university, classes, goals):
    """
    Creates a new user with the provided email and password.

    Args:
        email (str): The email address of the user.
        password (str): The password for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        university (str): The university the user is attending.
        classes (list): A list of classes for the user.
        goals (list): A list of goals for the user.

    Returns:
        user: The newly created user object.

    """
    user = auth.create_user(email=email, password=password)
    create_user_document(user.uid, first_name, last_name,
                         email, university, classes, goals)
    return user


def verify_user(email, password):
    # This function would typically also need to verify the password in a real app, which requires custom authentication system logic.
    user = auth.get_user_by_email(email)
    return user
