from flask import Blueprint, render_template

from apifairy import response
from flask_login import login_required

from {{ cookiecutter.project_slug }}.blueprints.user.models import User
from {{ cookiecutter.project_slug }}.blueprints.token.utils import token_auth
from {{ cookiecutter.project_slug }}.blueprints.user.decorators import role_required
from {{ cookiecutter.project_slug }}.blueprints.user.schemas import user_schema, users_schema

admin = Blueprint("admin", __name__, template_folder="templates")

# -----------------------------------------------------------------------------
# REST ROUTES
# -----------------------------------------------------------------------------


@admin.route("/api/users")
@token_auth.login_required(role=["admin"])
@response(users_schema)
def users():
    """Retrieve all users"""
    users = User.query.all()

    return users


@admin.route("/api/users/<id>")
@token_auth.login_required(role=["admin"])
@response(user_schema)
def user_detail(id):
    """Retrieve user detail"""
    user = User.find_by_id(id)

    return user


# -----------------------------------------------------------------------------
# WEB ROUTES
# -----------------------------------------------------------------------------


@admin.route("/admin")
@login_required
@role_required("admin")
def index():
    context = {"users": User.query.all()}
    return render_template("admin/index.html", context=context)
