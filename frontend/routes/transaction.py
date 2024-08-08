from .. import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from frontend.forms import TransactionForm
from datetime import datetime
from requests import post, get


@app.get("/change_balance")
@login_required
def get_transaction():
    form = TransactionForm()
    user = current_user.nickname
    return render_template("income.html", form=form, user=user)


@app.post("/change_balance")
@login_required
def post_transcation():
    form = TransactionForm()
    if form.validate_on_submit():
        print(type(form.amount.data))

        data = {
            "owner": current_user.nickname,
            "amount": form.amount.data,
            "category": form.category.data
        }
        response = post("http://backend:8000/change_balance", json=data)
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            return (f"Error {response.status_code} {response.json().get('detail')}")
    return render_template("income.html", form=form, user=current_user.nickname)
