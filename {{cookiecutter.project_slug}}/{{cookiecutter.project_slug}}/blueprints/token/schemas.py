from marshmallow import validate

from {{ cookiecutter.project_slug }}.extensions import marshmallow as ma
from {{ cookiecutter.project_slug }}.blueprints.token.models import Token


class TokenSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Token
        ordered = True

    id = ma.auto_field(dump_only=True)
    token = ma.auto_field(dump_only=True)
    token_expiration = ma.auto_field(dump_only=True)


token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)


class TokenRequestSchema(ma.Schema):
    email = ma.String(required=True, validate=[validate.Email()])
    password = ma.String(required=True)


token_request_schema = TokenRequestSchema()
