from flask import Flask
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix
from celery import Celery

from {{ cookiecutter.project_slug }}.blueprints.page.views import page
from {{ cookiecutter.project_slug }}.blueprints.up.views import up
from {{ cookiecutter.project_slug }}.blueprints.user import user
from {{ cookiecutter.project_slug }}.blueprints.invite import invite
from {{ cookiecutter.project_slug }}.blueprints.billing import billing
from {{ cookiecutter.project_slug }}.blueprints.user.models import User
from {{ cookiecutter.project_slug }}.blueprints.admin import admin
from {{ cookiecutter.project_slug }}.blueprints.token import token
from {{ cookiecutter.project_slug }}.blueprints.cmd import cmd
from {{ cookiecutter.project_slug }}.extensions import db
from {{ cookiecutter.project_slug }}.extensions import apifairy
from {{ cookiecutter.project_slug }}.extensions import marshmallow
from {{ cookiecutter.project_slug }}.extensions import flask_static_digest
from {{ cookiecutter.project_slug }}.extensions import login_manager
from {{ cookiecutter.project_slug }}.extensions import mail
from {{ cookiecutter.project_slug }}.extensions import toolbar


def create_celery_app(app=None):
    """
    Create a new Celery app and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, static_folder="../public", static_url_path="")

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    middleware(app)
    app.register_blueprint(up)
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(token)
    app.register_blueprint(billing)
    app.register_blueprint(invite)
    app.register_blueprint(admin)
    app.register_blueprint(cmd)
    extensions(app)
    authentication(app, User)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    db.init_app(app)
    flask_static_digest.init_app(app)
    marshmallow.init_app(app)
    apifairy.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    toolbar.init_app(app)

    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Enable the Flask interactive debugger in the brower for development.
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    # Set the real IP address into request.remote_addr when behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def authentication(app, user_model):
    """
    Initialize Flask-Login extension (this mutates the app passed in)

    :param app: Flask application instance
    :param user_model: Model that contains the authentication info
    :return: None
    """
    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(uuid):
        """
        Flask-Login is database agnostic, so it expects a little help
        determining how to find a user. This allows for usage of
        `current_user`, `is_authenticated`, `is_anonymous`, etc in
        the application.

        :param uuid: uuid
        :return: User instance
        """
        return user_model.query.get(uuid)


celery_app = create_celery_app()
