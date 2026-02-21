from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_number: str
    account_holder_name: str
    balance: float
