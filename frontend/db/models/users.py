from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_login import UserMixin
from .. import Base


class User(Base, UserMixin):
    __tablename__ = 'users'
    nickname: Mapped[str]
    password: Mapped[str]
