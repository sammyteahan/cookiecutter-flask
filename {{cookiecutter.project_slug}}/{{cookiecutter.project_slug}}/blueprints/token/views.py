import jwt
import pytz
from datetime import datetime, timedelta

from apifairy import body
from flask import Blueprint, request, jsonify, current_app

from {{ cookiecutter.project_slug }}.blueprints.token.models import Token
from {{ cookiecutter.project_slug }}.blueprints.token.schemas import token_request_schema

token = Blueprint("token", __name__, template_folder="templates")


@token.route("/api/tokens", methods=["POST"])
@body(token_request_schema)
def token_create(args):
    """Create new JWT Token"""
    from {{ cookiecutter.project_slug }}.blueprints.user.models import User
    user = User.find_by_email(args.get("email"))

    if not user or not user.authenticated(password=args.get("password")):
        return jsonify(success=False, message="Wrong email or password")

    if not user.is_active():
        return jsonify(success=False, message="This account has been disabled")

    refresh_expiration = datetime.now(
        pytz.utc) + timedelta(days=current_app.config["REFRESH_TOKEN_EXP"])

    access_token = jwt.encode(
        {
            "email": user.email,
            "role": user.role,
            "iss": request.host,
            "iat": datetime.now(pytz.utc),
            "exp": datetime.now(pytz.utc) +
            timedelta(minutes=current_app.config["ACCESS_TOKEN_EXP"]),
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )
    refresh_token = jwt.encode(
        {
            "iss": request.host,
            "iat": datetime.now(pytz.utc),
            "exp": refresh_expiration,
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    user.update_tracking_activity(request.remote_addr)
    Token.create(user=user, jwt=refresh_token, expiration=refresh_expiration)

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
    )
