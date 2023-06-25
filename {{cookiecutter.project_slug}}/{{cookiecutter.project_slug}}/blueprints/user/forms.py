from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    next = HiddenField()
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class PasswordForgotForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(8, 128)])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirmation", message="Passwords must match")
        ])
    password_confirmation = PasswordField(
        "Password Confirmation", validators=[DataRequired()])
    submit = SubmitField("Submit")
