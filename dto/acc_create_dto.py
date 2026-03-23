from pydantic import BaseModel

class AccountCreate(BaseModel):
    accountId   : str
    bankId  : str
    entityId  : str
    entityName  : str
    bankName  : str
