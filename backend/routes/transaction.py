from .. import app
from sqlalchemy import select, update, and_
from backend.db import Transaction, Wallet, Session
from backend.schemas import TransData, WalletData, UserData, TransAdd, Filtered
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
def add_income(data: TransAdd):
    with Session.begin() as session:
        data.date = datetime.fromisoformat(data.date)
        income = Transaction(**data.model_dump())
        session.add(income)
        wallet = session.scalar(select(Wallet).where(Wallet.owner == data.owner))
        balance = wallet.balance + data.amount
        if balance >= 0 and balance <= 5:
            raise HTTPException(417, detail="you can't exceed the unreachable reserve")
        if balance < 0:
            raise HTTPException(417, detail="You haven`t enough money for that")
        upd = update(Wallet).where(Wallet.owner == data.owner).values(balance=balance)
        session.execute(upd)
        

@app.get("/get_trans")
def trans_list(data: UserData):
    with Session.begin() as session:
        transactions = session.scalars(select(Transaction).where(Transaction.owner == data.user)).all()
        if transactions != None:
            transactions = [TransData.model_validate(item) for item in transactions]
            return transactions
        return transactions
    

@app.post("/filters")
def filters(data: Filtered):
    with Session.begin() as session:
        start_date = data.start_date
        end_date = data.end_date
        filtered = session.query(Transaction).filter(Transaction.date.between(start_date, end_date)).filter(Transaction.owner == data.owner)
        filtered = [TransData.model_validate(item) for item in filtered]
        return filtered