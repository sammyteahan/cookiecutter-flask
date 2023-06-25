from flask import Blueprint

from apifairy import response, body

from lib.util_schema import api_message_schema
from {{ cookiecutter.project_slug }}.blueprints.user.models import User
from {{ cookiecutter.project_slug }}.blueprints.token.utils import token_auth
from {{ cookiecutter.project_slug }}.blueprints.invite.schemas import invite_create_schema

invite = Blueprint("invite", __name__, template_folder="templates")


# -----------------------------------------------------------------------------
# REST ROUTES
# -----------------------------------------------------------------------------


@invite.route("/api/invites", methods=["POST"])
@token_auth.login_required(role=["manager"])
@body(invite_create_schema)
@response(api_message_schema)
def new_user(args):
    """Invite a new team member"""
    new_user = User.find_by_email(args.get("email"))

    if not new_user:
        params = {
            "email": args.get("email"),
            "password": User.set_unusable_password(),
            "active": False,
        }
        new_user = User(**params).save()
        token = new_user.serialize_token()
        User.initialize_registration(new_user, token)

    return {
        "success": True,
        "message": "Invite sent"
    }
