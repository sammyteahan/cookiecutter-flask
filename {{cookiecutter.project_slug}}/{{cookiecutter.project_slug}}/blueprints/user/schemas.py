from marshmallow import validate

from {{ cookiecutter.project_slug }}.extensions import marshmallow as ma
from {{ cookiecutter.project_slug }}.blueprints.user.models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    id = ma.auto_field(dump_only=True)
    email = ma.String(required=True)
    password = ma.String(required=True, load_only=True)
    role = ma.auto_field(dump_only=True)
    sign_in_count = ma.Integer()
    current_sign_in_ip = ma.String()
    last_sign_in_ip = ma.String()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class PasswordResetSchema(ma.Schema):
    email = ma.String(required=True, validate=[validate.Email()])


password_reset_schema = PasswordResetSchema()
