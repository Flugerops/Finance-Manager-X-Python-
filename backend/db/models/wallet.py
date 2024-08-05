from .. import Base
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(Base):
    __tablename__ = "wallets"
    owner: Mapped[str]
    balance: Mapped[float]