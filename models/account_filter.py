from sqlalchemy import Column, String
from database.db import Base

class AccountFilter(Base):
    __tablename__ = "acc_filter_tb"

    accountId = Column(String, primary_key=True, index=True)
    blockingLevel = Column(String)   # BLACK / GREY
    reason = Column(String)