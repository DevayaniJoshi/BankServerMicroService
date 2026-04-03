from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.settings import KAFKA_TRANSACTION_TOPIC
from database.db import get_db
from models.transaction import Transaction
from dto.transaction_create_dto import TransactionCreateDTO
from dto.transaction_response_dto import TransactionResponseDTO
from dto.transaction_update_dto import TransactionUpdateDTO
from uuid import UUID
from config.kafka_config import get_kafka_producer
from config.settings import ENABLE_KAFKA
from models.account import Account

router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"]
)

# CREATE
@router.post("/", response_model=TransactionResponseDTO)
def create_transaction(transaction: TransactionCreateDTO, db: Session = Depends(get_db)):

    # 🔥 STEP 1: Account Validation (Sender)
    account = db.query(Account).filter(
        Account.accountId == transaction.fromAccount
    ).first()

    if not account:
        raise HTTPException(status_code=400, detail="Sender account does not exist")

    # 🔥 STEP 1: Account Validation (Receiver)
    account = db.query(Account).filter(
        Account.accountId == transaction.toAccount
    ).first()

    if not account:
        raise HTTPException(status_code=400, detail="Receiver account does not exist")

    # 🔥 STEP 2: Filter Check
    from models.account_filter import AccountFilter

    filter_entry = db.query(AccountFilter).filter(
        AccountFilter.accountId == transaction.fromAccount
    ).first()

    filter_entry = db.query(AccountFilter).filter(
        AccountFilter.accountId == transaction.toAccount
    ).first()

    # 🔥 STEP 3: Status Decision
    if filter_entry:
        if filter_entry.blockingLevel.upper() == "BLACK":
            status = "BLOCKED"
        elif filter_entry.blockingLevel.upper() == "GREY":
            status = "REVIEW"
        else:
            status = "SUCCESS"
    else:
        status = "SUCCESS"

    try:
        new_transaction = Transaction(**transaction.model_dump())

        # 🔥 ADD STATUS
        new_transaction.status = status

        print(new_transaction)

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        if ENABLE_KAFKA:
            kafka = get_kafka_producer()
            kafka.send(
                KAFKA_TRANSACTION_TOPIC,
                TransactionResponseDTO.model_validate(new_transaction).model_dump(mode="json")
            )

        return new_transaction

    except Exception as e:
        print("ERROR: ", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# GET ALL
@router.get("/", response_model=list[TransactionResponseDTO])
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


# 🔥 ANALYTICS API (NEW)
@router.get("/stats")
def get_transaction_stats(db: Session = Depends(get_db)):

    transactions = db.query(Transaction).all()

    blocked_count = 0
    review_count = 0
    rejected_count = 0
    txn_ids = []

    for txn in transactions:
        status = txn.status.upper()

        if status == "BLOCKED":
            blocked_count += 1
            txn_ids.append(str(txn.transactionId))

        elif status == "REVIEW":
            review_count += 1
            txn_ids.append(str(txn.transactionId))

        elif status == "REJECTED":
            rejected_count += 1
            txn_ids.append(str(txn.transactionId))

    return {
        "blocked_count": blocked_count,
        "review_count": review_count,
        "rejected_count": rejected_count,
        "transaction_ids": txn_ids
    }


# 🔥 GET LAST N TRANSACTIONS
@router.get("/last/{accountId}", response_model=list[TransactionResponseDTO])
def get_last_n_transactions(
    accountId: str,
    limit: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.accountId == accountId
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    transactions = db.query(Transaction).filter(
        Transaction.fromAccount == accountId
    ).order_by(
        Transaction.timestamp.desc()
    ).limit(limit).all()

    return transactions


# GET BY ID
@router.get("/{transactionId}", response_model=TransactionResponseDTO)
def get_transaction(transactionId: UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(
        Transaction.transactionId == transactionId
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


# PATCH - Partial Update
@router.patch("/{transactionId}", response_model=TransactionResponseDTO)
def update_transaction(
    transactionId: UUID,
    updated_data: TransactionUpdateDTO,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.transactionId == transactionId
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# DELETE
@router.delete("/{transactionId}")
def delete_transaction(transactionId: UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(
        Transaction.transactionId == transactionId
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}