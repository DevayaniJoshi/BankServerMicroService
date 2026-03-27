from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.settings import KAFKA_TRANSACTION_TOPIC
from database.db import get_db
from models.transaction import Transaction
from dto.transaction_create_dto import TransactionCreateDTO
from dto.transaction_response_dto import TransactionResponseDTO
from dto.transaction_update_dto import TransactionUpdateDTO
from fastapi import HTTPException
from uuid import UUID
from config.kafka_config import get_kafka_producer
from fastapi import HTTPException


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"]
)

# CREATE
@router.post("/", response_model=TransactionResponseDTO)
def create_transaction(transaction: TransactionCreateDTO, db: Session = Depends(get_db)):
    try:

        new_transaction = Transaction(**transaction.model_dump())

        print(new_transaction)

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        kafka = get_kafka_producer()
        kafka.send(KAFKA_TRANSACTION_TOPIC,TransactionResponseDTO.model_validate(new_transaction).model_dump(mode="json"))

        return new_transaction
        
    except Exception as e:
        print("ERROR: ",e)
        raise HTTPException(
            status_code=500,
            detail=e.__cause__
        )

# GET ALL
@router.get("/", response_model=list[TransactionResponseDTO])
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


# GET BY ID
@router.get("/{transactionId}", response_model=TransactionResponseDTO)
def get_transaction(transactionId: UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.transactionId == transactionId).first()
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
    transaction = db.query(Transaction).filter(Transaction.transactionId == transactionId).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}