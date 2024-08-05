from .. import app
from flask import render_template
from flask_login import current_user, login_required
from requests import get



@app.get("/")
@login_required
def index():
    print(current_user.nickname)
    try:
        user = current_user.nickname
    except:
        user = None
        
    data = {
        "user": current_user.nickname
    }
    response = get("http://127.0.0.1:8000/balance", json=data)
    print(response.json())
    return render_template("index.html", user=user, balance=response.json())
