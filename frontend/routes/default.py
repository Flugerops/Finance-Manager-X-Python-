from .. import app
from flask import render_template
from flask_login import current_user, login_required
from requests import get



@app.get("/")
@login_required
def index():
    user = current_user.nickname
    data = {
        "user": user
    }
    balance = get("http://127.0.0.1:8000/balance", json=data)
    transactions = {
        "transactions": get("http://127.0.0.1:8000/get_trans", json=data).json()
    }
    print(transactions)
    return render_template("index.html", **transactions, user=user, balance=balance.json())
