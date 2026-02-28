from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class TransactionResponseDTO(BaseModel):
    transactionId: UUID
    timestamp: datetime
    fromBank: str
    fromAccount: str
    toBank: str
    toAccount: str
    amountReceived: float
    receivingCurrency: str
    amountPaid: float
    paymentCurrency: str
    paymentFormat: str

    class Config:
        from_attributes = True