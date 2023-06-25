import pytest
from werkzeug.security import generate_password_hash

from config import settings
from {{ cookiecutter.project_slug }}.app import create_app
from {{ cookiecutter.project_slug }}.extensions import db as _db
from {{ cookiecutter.project_slug }}.blueprints.user.models import User


@pytest.fixture(scope="session")
def app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """
    db_uri = settings.SQLALCHEMY_DATABASE_URI

    if "?" in db_uri:
        db_uri = db_uri.replace("?", "_test?")
    else:
        db_uri = f"{db_uri}_test"

    params = {
        "DEBUG": False,
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": db_uri,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope="session")
def db(app):
    """
    Setup our database, this only gets executed once per session.
    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()

    ##
    # create a user for some of our basic tests
    #
    params = {
        "role": "admin",
        "email": "admin@{{ cookiecutter.project_slug }}.com",
        "password": generate_password_hash("password"),
    }

    user = User(**params).save()

    _db.session.add(user)
    _db.session.commit()

    return _db


@pytest.fixture(scope="function")
def session(db):
    """
    Allow very fast tests by using rollbacks and nested sessions. This does
    require that your database supports SQL savepoints, and Postgres does.
    Read more about this at:
    http://stackoverflow.com/a/26624146
    :param db: Pytest fixture
    :return: None
    """
    db.session.begin_nested()

    yield db.session

    db.session.rollback()


@pytest.fixture(scope="session")
def token(db):
    """
    Serializes a JWS token

    :param db: PyTest fixture
    :return: JWS Token
    """
    user = User.find_by_email("admin@{{ cookiecutter.project_slug }}.com")
    return user.serialize_token()


@pytest.fixture(scope="function")
def users(db):
    """
    Create user fixtures

    :param db: PyTest fixture
    :return: SQLAlchemy database session
    """
    db.session.query(User).delete()
    db.session.query(Team).delete()

    users = [
        {
            "role": "admin",
            "email": "admin@{{ cookiecutter.project_slug }}.com",
            "password": generate_password_hash("password"),
        },
        {
            "role": "manager",
            "email": "disabled@{{ cookiecutter.project_slug }}.com",
            "password": generate_password_hash("password"),
            "active": False,
        }
    ]

    for user in users:
        db.session.add(User(**user))

    db.session.commit()

    return db
