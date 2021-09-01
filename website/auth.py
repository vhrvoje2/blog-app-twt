from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.sql.functions import user
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_data = request.form.get("email")
        password_data = request.form.get("password")

        user = User.query.filter_by(email=email_data).first()
        if user:
            if check_password_hash(user.password, password_data):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email doesn't exist.", category="error")
    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email_data = request.form.get("email")
        username_data = request.form.get("username")
        password_data = request.form.get("password")
        repeat_password_data = request.form.get("repeat_password")

        email_exists = True if User.query.filter_by(email=email_data).first() else False
        username_exists = True if User.query.filter_by(username=username_data).first() else False
        if email_exists:
            flash("Email is already in use.", category="error")
        elif username_exists:
            flash("Username is already in use.", category="error")
        elif password_data != repeat_password_data:
            flash("Passwords don't match!", category="error")
        elif len(username_data) < 2:
            flash("Username is too short", category="error")
        elif len(password_data) < 6:
            flash("Password is too short", category="error")
        elif len(email_data) < 4:
            flash("Email is invalid.", category="error")
        else:
            new_user = User(username=username_data, email=email_data, password=generate_password_hash(password_data, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created")
            return redirect(url_for("views.home"))

    return render_template("signup.html")

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))
