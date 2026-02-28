from pydantic import BaseModel
from typing import Optional


class AccountUpdate(BaseModel):
    accountId   :Optional[int] = None
    bankId  : Optional[int] = None
    entityId  : Optional[int] = None 
    entityName  : Optional[str] = None
    bankName  : Optional[str] = None
