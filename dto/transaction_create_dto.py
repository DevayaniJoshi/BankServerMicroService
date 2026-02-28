from pydantic import BaseModel

class TransactionCreateDTO(BaseModel):
    fromBank: str
    fromAccount: str
    toBank: str
    toAccount: str
    amountReceived: float
    receivingCurrency: str
    amountPaid: float
    paymentCurrency: str
    paymentFormat: str