from .. import app
from sqlalchemy import select, update
from backend.db import Transaction, Wallet, Session
from backend.schemas import TransData, WalletData, UserData
from datetime import datetime
from fastapi.exceptions import HTTPException


@app.get("/balance")
def get_balance(data: UserData):
    with Session.begin() as session:
        balance = session.scalar(select(Wallet).where(Wallet.owner == data.user))
        return balance.balance
    

@app.post("/user_reg")
def reg_user(data: WalletData):
    with Session.begin() as session:
        wallet = Wallet(**data.model_dump())
        session.add(wallet)


@app.post("/change_balance")
def add_income(data: TransData):
    with Session.begin() as session:
        data.date = datetime.fromisoformat(data.date)
        income = Transaction(**data.model_dump())
        session.add(income)
        wallet = session.scalar(select(Wallet).where(Wallet.owner == data.owner))
        balance = wallet.balance + data.amount
        if balance < 0:
            raise HTTPException(417, detail="You have no money left")
        upd = update(Wallet).where(Wallet.owner == data.owner).values(balance=balance)
        session.execute(upd)
        

