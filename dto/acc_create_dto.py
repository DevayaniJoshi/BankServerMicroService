from pydantic import BaseModel

class AccountCreate(BaseModel):
    accountId   : int
    bankId  : int
    entityId  : int
    entityName  : str
    bankName  : str
