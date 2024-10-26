from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models.user import User, db

def create_user(username, email, password):
    user_exists = db.session.query(
        db.session.query(User).filter(
            ((User.username == username) | (User.email == email)) & (User.deleted_at is None)
        ).exists()
    ).scalar()

    if user_exists:
        return None

    try:
        new_user = User(
            username=username,
            email=email,
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    except IntegrityError:
        db.session.rollback()
        return None


def get_all_users():
    return User.query.filter_by(deleted_at=None).all()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id, deleted_at=None).first()


def delete_user(user_id):
    user = get_user_by_id(user_id)

    if user:
        user.deleted_at = func.now()
        db.session.commit()
        return user

    return None
