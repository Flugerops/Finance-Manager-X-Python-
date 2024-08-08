from .. import app
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from requests import get, post
from datetime import datetime


@app.get("/")
@login_required
def index():
    user = current_user.nickname
    data = {
        "user": user
    }
    balance = get("http://backend:8000/balance", json=data)
    transactions = {
        "transactions": get("http://backend:8000/get_trans", json=data).json()
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
    balance = get("http://backend:8000/balance", json=data)
    try:
        start_date = request.form.get('start-date')
    except:
        redirect(url_for("index"))
    end_date = request.form.get('end-date')
    if not end_date:
        end_date = datetime.now().isoformat()

    data = {
        "owner": user,
        "start_date": start_date,
        "end_date": end_date
    }
    filtered = {
        "transactions": post("http://backend:8000/filters", json=data).json()
    }
    return render_template("index.html", **filtered, user=user, balance=balance.json())
