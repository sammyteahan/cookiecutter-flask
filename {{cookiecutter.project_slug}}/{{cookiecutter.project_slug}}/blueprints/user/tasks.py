from flask_mail import Message
from flask import render_template

from {{ cookiecutter.project_slug }}.extensions import mail
from {{ cookiecutter.project_slug }}.app import celery_app as celery
from {{ cookiecutter.project_slug }}.blueprints.user.models import User


def send_email(subject, sender, recipient, text_body):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = text_body
    mail.send(msg)


@celery.task(name="deliver_password_reset")
def deliver_password_reset(user_id, token):
    user = User.find_by_id(user_id)
    ctx = {"user": user, "token": token}
    send_email(
        "Headshots.ai Password Reset",
        "admin@mail.headshots.ai",
        user.email,
        render_template("user/email/password_reset.txt", ctx=ctx)
    )
