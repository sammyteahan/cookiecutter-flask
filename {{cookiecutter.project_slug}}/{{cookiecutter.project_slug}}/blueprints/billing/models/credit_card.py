import uuid

from sqlalchemy.dialects.postgresql import UUID

from {{ cookiecutter.project_slug }}.extensions import db
from lib.util_sqlalchemy import ResourceMixin
from lib.util_datetime import timedelta_months


class CreditCard(ResourceMixin, db.Model):
    IS_EXPIRING_DELTA = 2

    __tablename__ = "cards"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    brand = db.Column(db.String(32))
    last4 = db.Column(db.Integer())
    expiration_date = db.Column(db.Date, index=True)
    is_expiring = db.Column(db.Boolean(), nullable=False, server_default="0")

    # Relationships
    user_id = db.Column(
        UUID,
        db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=True
    )

    @classmethod
    def is_expiring_soon(cls, compare_date=None, expiration_date=None):
        """
        Determine whether or not a card is expiring soon.

        :param compare_date: Date to compare
        :param expiration_date: Expiration date
        :return: bool
        """
        return expiration_date <= timedelta_months(
            CreditCard.IS_EXPIRING_DELTA, compare_date=compare_date)
