from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from trivion import db, bcrypt
from trivion.Models import User, Game
from trivion.users.Forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm)
from trivion.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

GET = "GET"
POST = "POST"

LOGIN = "Login.html"
REGISTER = "Register.html"
ACCOUNT = "Account.html"
USER_GAMES = "UserGames.html"
RESET_REQUEST = "ResetRequest.html"
RESET_TOKEN = "ResetToken.html"


@users.route("/", methods=[GET, POST])
@users.route("/login", methods=[GET, POST])
def login():
    """
    Login page route with login form
    :return: Home.html template if success, else, showing errors
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template(LOGIN, title="Login", form=form)


@users.route("/logout")
def logout():
    """
    Redirect to home page
    :return: home route
    """
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/register", methods=[GET, POST])
def register():
    """
    Register page route with Registration form
    :return: Login.html template if success, else, showing errors
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You are now logged in.", "success")
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home"))
    return render_template(REGISTER, title="Register", form=form)


@users.route("/account", methods=[GET, POST])
@login_required
def account():
    """
    Account page route with option to update info
    :return: Account.html template with new info if changed
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == GET:
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(ACCOUNT, title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_games(username):
    """
    User's games page route
    :param username: username
    :return: User's games
    """
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    games = Game.query.filter_by(name=user)\
        .order_by(Game.date_created.desc())\
        .paginate(page=page, per_page=5)
    return render_template(USER_GAMES, games=games, user=user)


@users.route("/reset_password", methods=[GET, POST])
def reset_request():
    """
    Reset password page route
    :return: email for resetting password
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template(RESET_REQUEST, title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=[GET, POST])
def reset_token(token):
    """
    Reset password unique token
    :param token: unique token
    :return: ResetToken.html
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated, you are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template(RESET_TOKEN, title="Reset Password", form=form)
