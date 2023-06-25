import os
from distutils.util import strtobool

SECRET_KEY = os.getenv("SECRET_KEY", None)
DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "8000"))
)

# SQLAlchemy.
pg_user = os.getenv("POSTGRES_USER", "postgres")
pg_pass = os.getenv("POSTGRES_PASSWORD", "password")
pg_host = os.getenv("POSTGRES_HOST", "postgres")
pg_port = os.getenv("POSTGRES_PORT", "5432")
pg_db = os.getenv("POSTGRES_DB", pg_user)
db = f"postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", db)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = DEBUG

# Redis.
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Celery
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": [
        "{{ cookiecutter.project_slug }}.blueprints.user.tasks",
        "{{ cookiecutter.project_slug }}.blueprints.invite.tasks",
    ]
}

# Seeds
SEED_ADMIN_EMAIL = str(os.getenv("SEED_ADMIN_EMAIL"))
SEED_ADMIN_PASSWORD = str(os.getenv("SEED_ADMIN_PASSWORD"))
SEED_MEMBER_EMAIL = str(os.getenv("SEED_MEMBER_EMAIL", "member@headshots.ai"))
SEED_MEMBER_PASSWORD = str(os.getenv("SEED_MEMBER_PASSWORD"))

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret")
ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP", 15))
REFRESH_TOKEN_EXP = int(os.getenv("REFRESH_TOKEN_EXP ", 7))

# API documentation
APIFAIRY_TITLE = "{{ cookiecutter.project_slug }} API"
APIFAIRY_VERSION = "0.1.0"
APIFAIRY_UI = os.environ.get("DOCS_UI", "redoc")
APIFAIRY_TAGS = ["user"]

# Flask-Mail
MAIL_SERVER = os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io")
MAIL_PORT = os.getenv("MAIL_PORT", 2525)
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAUL_SENDER", "noreply@example.com")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = bool(strtobool(os.getenv("MAIL_USE_TLS", "true")))
MAIL_USE_SSL = bool(strtobool(os.getenv("MAIL_USE_SSL", "false")))

# DebugToolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# User
USER_UNUSABLE_PASSWORD = os.getenv("USER_UNUSABLE_PASSWORD")

# Billing
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_PLANS = {
    "0": {
        "id": "bronze",
        "name": "Bronze",
        "amount": 100,
        "currency": "usd",
        "interval": "month",
        "interval_count": 1,
        "trial_period_days": 14,
        "statement_descriptor": "",
        "metadata": {},
    },
    "1": {
        "id": "gold",
        "name": "Gold",
        "amount": 500,
        "currency": "usd",
        "interval": "month",
        "interval_count": 1,
        "trial_period_days": 14,
        "statement_descriptor": "",
        "metadata": {},
    },
    "2": {
        "id": "platinum",
        "name": "Platinum",
        "amount": 1000,
        "currency": "usd",
        "interval": "month",
        "interval_count": 1,
        "trial_period_days": 14,
        "statement_descriptor": "",
        "metadata": {},
    },
}
