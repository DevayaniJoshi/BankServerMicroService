from pydantic import BaseModel

class FilterDTO(BaseModel):
    accountId: str
    level: str
    reason: str