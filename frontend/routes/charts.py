from .. import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from requests import get


@app.get("/charts")
@login_required
def charts():
    user = current_user.nickname
    data = {
        "user": user
    }
    balance = get("http://127.0.0.1:8000/balance", json=data).json()
    transactions = get("http://127.0.0.1:8000/get_trans", json=data).json()
    data = [(item.get("date"), item.get("amount")) for item in transactions]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    incomes = [value for value in values if value > 0]
    expenses = [abs(value) for value in values if value < 0]
    incomes_sum = sum(incomes)
    expenses_sum = sum(expenses)
    return render_template(
        "charts.html", user=user, balance=balance, labels=labels, values=values, incomes=incomes, 
        expenses=expenses, incomes_sum=incomes_sum, expenses_sum=expenses_sum
    )