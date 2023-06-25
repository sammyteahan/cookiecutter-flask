from {{ cookiecutter.project_slug }}.extensions import marshmallow as ma


class MessageSchema(ma.Schema):
    success = ma.Boolean()
    message = ma.String()


api_message_schema = MessageSchema()
