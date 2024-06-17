from app.models import db, Users
from app.forms.user import UserLoginForm
from app.utils.login_utils import verify_password
from flask import session
from sqlalchemy.exc import SQLAlchemyError


def login(data: dict) -> (bool, str):
    """Login user"""

    try:

        user_form = UserLoginForm(data)

        if user_form.validate():
            results = db.session.execute(db.select(Users).where(Users.email == user_form.email.data))
            user = results.scalars().first()

            if user:
                if verify_password(user_form.password.data, user.password):
                    # Store session
                    session["username"] = user_form.email.data

                    return True, "Successfully SignedIn!"

            return False, "Incorrect username or password!"

    except SQLAlchemyError as ex:
        print(ex)
        return False, "Database error occurred!"


def logout(user_id: str):
    """Logout user"""
    return True, "Successfully SignedOut!"
