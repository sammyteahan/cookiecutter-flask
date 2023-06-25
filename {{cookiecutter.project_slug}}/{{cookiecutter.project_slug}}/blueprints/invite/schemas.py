from marshmallow import validate

from {{ cookiecutter.project_slug }}.extensions import marshmallow as ma


class InviteCreate(ma.Schema):
    email = ma.String(required=True, validate=[validate.Email()])


invite_create_schema = InviteCreate()
