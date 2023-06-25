from flask import Blueprint

from {{ cookiecutter.project_slug }}.blueprints.billing.models.payment import Payment  # noqa: F401
from {{ cookiecutter.project_slug }}.blueprints.billing.models.credit_card import (  # noqa: F401
    CreditCard
)
from {{ cookiecutter.project_slug }}.blueprints.billing.models.subscription import (  # noqa: F401
    Subscription
)

billing = Blueprint('billing', __name__, template_folder="templates")
