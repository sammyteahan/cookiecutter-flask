import uuid

from sqlalchemy.dialects.postgresql import UUID

from {{ cookiecutter.project_slug }}.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Payment(ResourceMixin, db.Model):
    __tablename__ = "payments"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    plan = db.Column(db.String(128), index=True)
    receipt_number = db.Column(db.String(128), index=True)
    description = db.Column(db.String())
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    currency = db.Column(db.String(8))
    tax = db.Column(db.Integer())
    total = db.Column(db.Integer())

    # de-normalize card details so we can display a list of payment history
    # properly even if no active subscription is present or if card has changed
    brand = db.Column(db.String(32))
    last4 = db.Column(db.Integer())
    expiration_date = db.Column(db.Date, index=True)

    # Relationships
    user_id = db.Column(
        UUID,
        db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=True
    )

    @classmethod
    def billing_history(cls, team=None):
        """
        Return the billing history for a specific team.

        :param team: Team for which you want to retrieve billing history
        :return: Payments
        """
        payments = Payment.query.filter(Payment.team_id == team.id) \
            .order_by(Payment.created_on.desc()).limit(10)

        return payments
