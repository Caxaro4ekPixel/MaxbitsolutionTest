from sqlalchemy.orm import Session
from models import User
from typing import Optional


def register_user_in_db(db: Session, name: str, login: str, telegram_id: int) -> None:
    user = User(name=name, login=login, telegram_id=telegram_id)
    db.add(user)
    db.commit()


def check_user_in_db(db: Session, telegram_id: int) -> Optional[User]:
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    return db.query(User).filter(User.login == login).first()
