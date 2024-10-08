from main import app
from sqlalchemy import select, update, and_
from db import Transaction, Wallet, Session
from schemas import TransData, WalletData, UserData, TransAdd, Filtered, TransDel
from datetime import datetime
from fastapi.exceptions import HTTPException


@app.get("/balance")
def get_balance(data: UserData):
    with Session.begin() as session:
        balance = session.scalar(
            select(Wallet).where(Wallet.owner == data.user))
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
        wallet = session.scalar(
            select(Wallet).where(Wallet.owner == data.owner))
        balance = wallet.balance + data.amount
        if balance >= 0 and balance <= 5 and data.amount < 0:
            raise HTTPException(
                417, detail="you can't exceed the unreachable reserve")
        if balance < 0:
            raise HTTPException(
                417, detail="You haven`t enough money for that")
        upd = update(Wallet).where(Wallet.owner ==
                                   data.owner).values(balance=balance)
        session.execute(upd)


@app.get("/get_trans")
def trans_list(data: UserData):
    with Session.begin() as session:
        transactions = session.scalars(select(Transaction).where(
            Transaction.owner == data.user)).all()
        if transactions != None:
            transactions = [TransData.model_validate(
                item) for item in transactions]
            return transactions
        return transactions


@app.post("/filters")
def filters(data: Filtered):
    with Session.begin() as session:
        start_date = data.start_date
        end_date = data.end_date
        filtered = session.query(Transaction).filter(Transaction.date.between(
            start_date, end_date)).filter(Transaction.owner == data.owner)
        filtered = [TransData.model_validate(item) for item in filtered]
        return filtered


@app.delete("/undo_trans")
def delete_trans(data: TransDel):
    with Session.begin() as session:
        transaction = session.scalar(
            select(Transaction).where(Transaction.id == data.id))
        if data.owner != transaction.owner:
            raise HTTPException(status_code=403, detail="Permission denied")
        balance = session.scalar(
            select(Wallet).where(Wallet.owner == data.owner))
        if transaction.amount > 0:
            balance.balance -= transaction.amount
        elif transaction.amount < 0:
            balance.balance -= transaction.amount
        upd = update(Wallet).where(Wallet.owner ==
                                   data.owner).values(balance=balance.balance)
        session.delete(transaction)
        session.execute(upd)
        return "Transaction deleted"
