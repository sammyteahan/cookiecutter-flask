from flask import Blueprint, request, render_template, flash, redirect, url_for

from flask_login import login_user, logout_user
from apifairy import response, authenticate, body

from lib.safe_next_url import safe_next_url
from lib.util_schema import api_message_schema
from {{ cookiecutter.project_slug }}.blueprints.user.models import User
from {{ cookiecutter.project_slug }}.blueprints.token.utils import token_auth
from {{ cookiecutter.project_slug }}.blueprints.user.decorators import anonymous_required
from {{ cookiecutter.project_slug }}.blueprints.user.schemas import user_schema, password_reset_schema
from {{ cookiecutter.project_slug }}.blueprints.user.forms import (
    LoginForm,
    PasswordForgotForm,
    PasswordResetForm,
    RegistrationForm,
)

user = Blueprint("user", __name__, template_folder="templates")

# -----------------------------------------------------------------------------
# REST ROUTES
# -----------------------------------------------------------------------------


@user.route("/api/current_user", methods=["GET"])
@authenticate(token_auth)
@response(user_schema)
def user_info():
    """Current User"""
    email = token_auth.current_user()["email"]
    user = User.find_by_email(email)

    return user


@user.route("/api/reset-password", methods=["POST"])
@body(password_reset_schema)
@response(api_message_schema)
def reset(args):
    email = args.get("email")
    User.initialize_password_reset(email)

    return {
        "success": True,
        "message": "password reset email sent"
    }


# -----------------------------------------------------------------------------
# WEB ROUTES
# -----------------------------------------------------------------------------


@user.route("/login", methods=["GET", "POST"])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get("next"))

    if form.validate_on_submit():
        user = User.find_by_email(email=form.email.data)

        if user is None or not user.authenticated(password=form.password.data):
            flash("Email or password incorrect", "error")
            return redirect(url_for("user.login"))

        if not user.is_active():
            flash("This account has been disabled", "error")
            return redirect(url_for("user.login"))

        login_user(user, remember=True)
        user.update_tracking_activity(request.remote_addr)

        next_url = request.form.get("next")

        if next_url:
            return redirect(safe_next_url(next_url))

        return redirect(url_for("page.home"))

    return render_template("user/login.html", form=form)


@user.route("/logout")
def logout():
    logout_user()
    flash("You have been signed out", "info")
    return redirect(url_for("user.login"))


@user.route("/forgot-password", methods=["GET", "POST"])
@anonymous_required()
def forgot_password():
    form = PasswordForgotForm()

    if form.validate_on_submit():
        User.initialize_password_reset(form.email.data)
        flash("A password reset link has been sent to your email", "success")
        return redirect(url_for("user.login"))

    return render_template("user/forgot.html", form=form)


@user.route("/reset-password", methods=["GET", "POST"])
@anonymous_required()
def reset_password():
    form = PasswordResetForm(reset_token=request.args.get("reset_token"))

    if form.validate_on_submit():
        user = User.deserialize_token(request.form.get("reset_token"))

        if user is None:
            flash("Reset link expired or tampered with", "error")
            return redirect(url_for("user.forgot_password"))

        user.password = User.encrypt_password(form.password.data)
        user.save()

        if login_user(user):
            flash("Your password has been reset", "success")
            return redirect(url_for("page.home"))

    return render_template("user/reset.html", form=form)


@user.route("/register/<uuid:user_id>/<token>", methods=["GET", "POST"])
@anonymous_required()
def register(user_id, token):
    """
    Allow a user to register after receiving an invitation email

    :param user_id: uuid
    :param token: encoded token from email link
    """
    user = User.find_by_id(user_id)
    form = RegistrationForm(data={"email": user.email})

    if form.validate_on_submit():
        validated_user_token = User.deserialize_token(token, expiration=14400)

        if validated_user_token is None:
            flash("Invite link expired", "error")
            return redirect(url_for("user.login"))

        form.populate_obj(user)
        user.password = User.encrypt_password(form.password.data)
        user.active = True
        user.save()

        if login_user(user):
            flash("You have succesfully registered", "success")
            return redirect(url_for("page.home"))

    return render_template("user/register.html", form=form)
