from sqlalchemy import Column, Float, String, DateTime
from database.db import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Transaction(Base):
    __tablename__ = "transactions"

    transactionId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    timestamp = Column(String, nullable=False)
 
    fromBank = Column(String, nullable=False)
    fromAccount = Column(String, nullable=False)

    toBank = Column(String, nullable=False)
    toAccount = Column(String, nullable=False)

    amountReceived = Column(Float, nullable=False)
    receivingCurrency = Column(String, nullable=False)

    amountPaid = Column(Float, nullable=False)
    paymentCurrency = Column(String, nullable=False)

    paymentFormat = Column(String, nullable=False)

    status = Column(String, default="SUCCESS")