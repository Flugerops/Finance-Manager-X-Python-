from .. import app
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from frontend.forms import RegisterForm, LoginForm
from sqlalchemy import select
from frontend.db import Session, User
from requests import post


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            user = User(nickname=user.nickname)
            return user


@app.get('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.post('/register')
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.scalar(select(User).where(
                User.nickname == form.nickname.data))
            if user:
                flash("User exists!")
                return redirect(url_for('register'))
            user = User(
                nickname=form.nickname.data,
                password=form.password.data
            )
            data = {
                "owner": form.nickname.data
                
            }
            session.add(user)
            response = post("http://backend:8000/user_reg", json=data)
            if response.status_code == 200:
                return redirect(url_for("index"))
            else:
                return response.status_code
    return render_template('register.html', form=form)


@app.get('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.post('/login')
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.query(User).where(
                User.nickname == form.nickname.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for("index"))
                flash("Wrong password")
            else:
                flash("Wrong nickname")
    return render_template('login.html', form=form)


@app.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
