import uuid
import pytz
import datetime
from collections import OrderedDict

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous import BadData, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

from {{ cookiecutter.project_slug }}.extensions import db
from lib.util_sqlalchemy import (
    ResourceMixin,
    AwareDateTime,
    SoftDeleteQueryManager,
)


class User(UserMixin, ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ("admin", "Admin"),
        ("member", "Member"),
    ])

    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(
        db.Enum(*ROLE, name="role_types", native_enum=False),
        index=True,
        nullable=False,
        server_default="member",
    )
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    is_removed = db.Column(db.Boolean(), default=False, nullable=False)

    # Activity Tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    # Relationships
    tokens = db.relationship("Token", back_populates="user")

    # Custom query class to decorate model with soft-delete functionality
    query_class = SoftDeleteQueryManager

    @classmethod
    def find_by_id(cls, id):
        """
        Find a user by their id

        :param id:
        :return: User instance
        """
        return User.query.get(id)

    @classmethod
    def find_by_email(cls, email):
        """
        Find a user by their email

        :param email:
        :return: User instance
        """
        return User.query.filter(User.email == email).first()

    @classmethod
    def encrypt_password(cls, plaintext_passwd):
        """
        Hash a plaintext string using PBKDF2

        :param paintext_passwd: password in plain text
        :return: str
        """
        if plaintext_passwd:
            return generate_password_hash(plaintext_passwd)

        return None

    @classmethod
    def initialize_password_reset(cls, email):
        """
        Initiate the password reset flow

        :param email: string
        :return: User
        """
        user = User.find_by_email(email)

        if not user:
            return

        reset_token = user.serialize_token()

        from {{ cookiecutter.project_slug }}.blueprints.user.tasks import deliver_password_reset
        deliver_password_reset.delay(user.id, reset_token)

        return user

    @classmethod
    def initialize_registration(cls, user, token):
        """
        Initiate the registration flow for a newly invited member

        :param user: User
        :param token:
        :return: User
        """
        from {{ cookiecutter.project_slug }}.blueprints.invite.tasks import deliver_registration_email
        deliver_registration_email.delay(user.id, token)

        return user

    @classmethod
    def deserialize_token(cls, token, expiration=3600):
        """
        Obtain a user from deserializing a timed token

        :param token: str
        :param expiration: int representing seconds, default to 1 hour
        :return: User
        """
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        try:
            decoded_token = serializer.loads(token, max_age=expiration)
            return User.find_by_email(decoded_token.get("email"))
        except (BadData, BadSignature, SignatureExpired):
            return None

    @classmethod
    def set_unusable_password(cls):
        """
        Create a password for users before they finish the registration process

        :return: str
        """
        return generate_password_hash(
            current_app.config.get("USER_UNUSABLE_PASSWORD"))

    def authenticated(self, with_password=True, password=""):
        """
        Ensure a user is authenticated, and optionally check their password

        :param with_password: optionally check the user password
        :param password: password to verify
        :return: bool
        """
        if with_password:
            return check_password_hash(self.password, password)

        return True

    def update_tracking_activity(self, ip_address):
        """
        Update various fields on the user that are related to meta
        data on their account

        :param ip_address:
        :return: SQLAchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()

    def serialize_token(self):
        """
        Create and sign a token that can be used for things such as resetting
        a password or other tasks that involve a one-off token

        :return: str
        """
        key = current_app.config.get("SECRET_KEY")

        serializer = URLSafeTimedSerializer(key)

        return serializer.dumps({"email": self.email})

    def is_active(self):
        """
        Return whether or not the user account is active.

        :return: bool
        """
        return self.active

    def delete(self):
        """
        Override `ResourceMixin` delete. This soft deletes the user instance

        :return: User
        """
        self.is_removed = True
        self.save()
