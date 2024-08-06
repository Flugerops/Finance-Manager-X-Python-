from .. import Base
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


class Transaction(Base):
    __tablename__ = "transactions"
    owner: Mapped[str]
    amount: Mapped[float]
    date: Mapped[date]
    category: Mapped[str]
    
    
