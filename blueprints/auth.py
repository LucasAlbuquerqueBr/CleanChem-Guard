from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from i18n import t
from models import User
from sheets_db import SheetsDB


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = SheetsDB.get()
        rec = db.get_user_by_username(username)
        if not rec or not check_password_hash(rec.get("password_hash", ""), password):
            flash(t("auth.invalid_credentials"))
            return render_template("login.html")
        user = User.from_record(rec)
        login_user(user)
        return redirect(url_for("index"))
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash(t("auth.required_fields"))
            return render_template("register.html")
        db = SheetsDB.get()
        if db.get_user_by_username(username):
            flash(t("auth.username_taken"))
            return render_template("register.html")
        ph = generate_password_hash(password)
        rec = db.create_user(username=username, email=email, password_hash=ph)
        login_user(User.from_record(rec))
        return redirect(url_for("index"))
    return render_template("register.html")


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.get("/u/<username>")
def user_page(username):
    db = SheetsDB.get()
    user = db.get_user_by_username(username)
    if not user:
        return render_template("user.html", user=None, posts=[])
    posts = db.list_posts(author_id=user.get("id"))
    return render_template("user.html", user=user, posts=posts)

