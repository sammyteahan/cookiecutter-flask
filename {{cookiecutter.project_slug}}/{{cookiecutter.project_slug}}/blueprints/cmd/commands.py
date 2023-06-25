import click
from flask import Blueprint
from werkzeug.security import generate_password_hash

from lib.util_cli import log_status
from {{ cookiecutter.project_slug }}.blueprints.user.models import User


cmd = Blueprint("cmd", __name__)


@cmd.cli.command("create-user")
@click.argument("email")
@click.argument("password")
def create(email, password):
    """ Create a User in the DB """
    click.echo("Working...")

    params = {
        "role": "member",
        "email": email,
        "password": generate_password_hash(password),
    }

    User(**params).save()

    log_status(1, "user")
