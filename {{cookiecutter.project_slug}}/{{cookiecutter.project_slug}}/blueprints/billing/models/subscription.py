import uuid

from sqlalchemy.dialects.postgresql import UUID

from {{ cookiecutter.project_slug }}.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Subscription(ResourceMixin, db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    plan = db.Column(db.String(128))

    # Relationships
    user_id = db.Column(
        UUID,
        db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=True
    )
