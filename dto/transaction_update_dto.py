from pydantic import BaseModel
from typing import Optional

class TransactionUpdateDTO(BaseModel):
    fromBank: Optional[str] = None
    fromAccount: Optional[str] = None
    toBank: Optional[str] = None
    toAccount: Optional[str] = None
    amountReceived: Optional[float] = None
    receivingCurrency: Optional[str] = None
    amountPaid: Optional[float] = None
    paymentCurrency: Optional[str] = None
    paymentFormat: Optional[str] = None