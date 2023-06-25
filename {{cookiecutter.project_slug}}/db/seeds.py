from flask import current_app

from werkzeug.security import generate_password_hash

from {{ cookiecutter.project_slug }}.blueprints.user.models import User

app_config = current_app.config


if User.find_by_email(app_config["SEED_ADMIN_EMAIL"]) is None:
    params = {
        "role": "admin",
        "name": "Admin User",
        "email": app_config["SEED_ADMIN_EMAIL"],
        "password": generate_password_hash(app_config["SEED_ADMIN_PASSWORD"]),
    }

    User(**params).save()

if User.find_by_email(app_config["SEED_MEMBER_EMAIL"]) is None:
    passwd = generate_password_hash(app_config["SEED_MEMBER_PASSWORD"])
    params = {
        "role": "member",
        "name": "Member User",
        "email": app_config["SEED_MEMBER_EMAIL"],
        "password": passwd,
    }

    User(**params).save()
