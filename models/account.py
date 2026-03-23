from sqlalchemy import Column, ForeignKey, String, String, Float
from database.db import Base


class Account(Base):
    __tablename__ = "accounts"   # Must match DB table name

    accountId    = Column(String, primary_key=True, index=True)
    bankId  = Column(String)
    entityId = Column(String)
    entityName = Column(String)
    bankName = Column(String)



