from sqlalchemy import Column, Integer, String, Float
from database.db import Base

class Account(Base):
    __tablename__ = "accounts"   # Must match DB table name

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    account_holder_name = Column(String)
    balance = Column(Float)
