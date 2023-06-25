from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
from flask_httpauth import HTTPTokenAuth
from flask_login import LoginManager
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
flask_static_digest = FlaskStaticDigest()
marshmallow = Marshmallow()
apifairy = APIFairy()
token_auth = HTTPTokenAuth()
login_manager = LoginManager()
mail = Mail()
toolbar = DebugToolbarExtension()
