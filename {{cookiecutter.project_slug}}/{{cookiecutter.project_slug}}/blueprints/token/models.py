import uuid

from sqlalchemy.dialects.postgresql import UUID

from {{ cookiecutter.project_slug }}.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Token(ResourceMixin, db.Model):
    """Model used for tracking refresh tokens"""
    __tablename__ = "tokens"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.Text, nullable=False)
    token_expiration = db.Column(db.DateTime, nullable=False)

    # Relationships
    user_id = db.Column(
        UUID,
        db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    user = db.relationship("User", back_populates="tokens")

    @classmethod
    def create(cls, user, jwt, expiration):
        return Token(
            user=user,
            token=jwt,
            token_expiration=expiration
        ).save()
