from pydantic import BaseModel
from typing import Optional


class AccountUpdate(BaseModel):
    accountId   :Optional[str] = None
    bankId  : Optional[str] = None
    entityId  : Optional[str] = None 
    entityName  : Optional[str] = None
    bankName  : Optional[str] = None
