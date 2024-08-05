from .. import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from frontend.forms import TransactionForm
from datetime import datetime
from requests import post


@app.get("/change_balance")
@login_required
def get_transaction():
    form = TransactionForm()
    return render_template("income.html", form=form)


@app.post("/change_balance")
@login_required
def post_transcation():
    form = TransactionForm()
    if form.validate_on_submit():
        data = {
            "owner": current_user.nickname,
            "amount": form.amount.data,
            "category": form.category.data
        }
        response = post("http://127.0.0.1:8000/change_balance", json=data)
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            return(f"Error {response.status_code} {response.json().get("detail")}")