from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.account import Account
from dto.acc_create_dto import AccountCreate
from dto.acc_update_dto import AccountUpdate

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

#create acc
@router.post("/", status_code =201)
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
@router.patch("/{account_id}")
def update_account(
    account_id: int,
    account: AccountUpdate,
    db: Session = Depends(get_db)
):
    db_account = db.query(Account).filter(Account.id == account_id).first()

    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update only provided fields
    if account.balance is not None:
        db_account.balance = account.balance

    if account.account_holder_name is not None:
        db_account.account_holder_name = account.account_holder_name

    db.commit()
    db.refresh(db_account)

    return db_account

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
