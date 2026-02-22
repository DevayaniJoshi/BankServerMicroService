from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.account import Account
from dto.acc_create_dto import AccountCreate

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)

#create acc
@router.post("/")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    new_account = Account(
        account_number=account.account_number,
        account_holder_name=account.account_holder_name,
        balance=account.balance
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


# GET single ACCOUNT
@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# GET ALL ACCOUNTS
@router.get("/")
def get_all_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return accounts


# UPDATE ACCOUNT 
# TODO:TESTING REQUIRED
@router.put("/{account_id}")
def update_account(account_id: int, balance: float, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance = balance
    db.commit()
    db.refresh(account)
    return account


# DELETE ACCOUNT
# TODO:TESTING REQUIRED
@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()
    return {"message": "Account deleted successfully"}
