from pydantic import BaseModel
from typing import Optional


class AccountUpdate(BaseModel):
    account_holder_name: Optional[str] = None
    balance: Optional[float] = None