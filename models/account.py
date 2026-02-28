from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database.db import Base

class Account(Base):
    __tablename__ = "accounts"   # Must match DB table name

    accountId    = Column(Integer, primary_key=True, index=True)
    bankId  = Column(Integer)
    entityId = Column(Integer)
    entityName = Column(String)
    bankName = Column(String)



