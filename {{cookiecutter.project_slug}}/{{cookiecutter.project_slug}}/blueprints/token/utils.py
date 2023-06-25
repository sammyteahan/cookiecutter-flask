import jwt

from flask import current_app

from {{ cookiecutter.project_slug }}.extensions import token_auth


@token_auth.get_user_roles
def get_user_roles(user):
    """
    Lookup user role, used in conjunction with
    the `login_required` decorated when used with
    roles.

    example:
        @login_required(role=["admin"])

    :param user:
    :return: str
    """
    return user["role"]


@token_auth.verify_token
def verify_token(token):
    """
    Verify the JWT token send in the Authorization header
    to ensure it hasn't expired or been tampered with

    :param token: str
    :return: dict of decoded token data
    """
    try:
        data = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        return False

    return data
