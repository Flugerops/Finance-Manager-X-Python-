from .. import app
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from requests import get, post



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
    return render_template("index.html", **transactions, user=user, balance=balance.json())


@app.post("/")
@login_required
def filter():
    action = request.form.get("action")
    if action == "reset":
        return redirect(url_for("index"))
    user = current_user.nickname
    data = {
        "user": user
    }
    balance = get("http://127.0.0.1:8000/balance", json=data)
    data = {
        "owner": user,
        "start_date": request.form.get('start-date'),
        "end_date": request.form.get('end-date')
    }
    filtered = {
        "transactions": post("http://127.0.0.1:8000/filters", json=data).json()
    }
    
    return render_template("index.html", **filtered, user=user, balance=balance.json())