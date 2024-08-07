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
    return render_template("charts.html", user=user, balance=balance)