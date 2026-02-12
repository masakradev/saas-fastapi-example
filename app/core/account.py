from pydantic import BaseModel

from app.modules.company.models import Company
from app.modules.user.models import User


class Account(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    user: User
    company: Company | None = None
