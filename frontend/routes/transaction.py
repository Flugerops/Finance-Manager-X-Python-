from .. import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from frontend.forms import TransactionForm
from datetime import datetime
from requests import post, get, delete


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
            detail = response.json().get('detail')
            return render_template("error.html", error=response.status_code, detail=detail)
    return render_template("income.html", form=form, user=current_user.nickname)


@app.get("/delete/<int:trans_id>")
@login_required
def delete_trans(trans_id):
    data = {
        "id": trans_id,
        "owner": current_user.nickname
    }
    remove_trans = delete("http://backend:8000/undo_trans", json=data)
    if remove_trans.status_code == 200:
        return redirect(url_for("index"))
    detail = remove_trans.json().get('detail')
    return render_template("error.html", error=remove_trans.status_code, detail=detail)
