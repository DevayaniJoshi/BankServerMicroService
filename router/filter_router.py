from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.account_filter import AccountFilter
from dto.filter_dto import FilterDTO


router = APIRouter(prefix="/api/account/filter", tags=["Filter"])


@router.get("/{accountId}")
def get_filter_by_account(accountId: str, db: Session = Depends(get_db)):
    
    account = db.query(AccountFilter).filter(
        AccountFilter.accountId == accountId
    ).first()

    # ✅ If NOT in filter → WHITELIST
    if not account:
        return {
            "accountId": accountId,
            "status": "WHITELISTED",
            "message": "Account is not in filter"
        }

    # ✅ If present → return filter details
    return {
        "accountId": account.accountId,
        "status": account.blockingLevel,
        "reason": account.reason
    }

@router.post("/")
def add_filter(data: FilterDTO, db: Session = Depends(get_db)):

    existing = db.query(AccountFilter).filter(
        AccountFilter.accountId == data.accountId
    ).first()

    # ✅ If exists → UPDATE
    if existing:
        existing.blockingLevel = data.level
        existing.reason = data.reason

        db.commit()
        db.refresh(existing)

        return {"message": "Filter updated successfully"}

    # ✅ If not exists → INSERT
    new_entry = AccountFilter(
        accountId=data.accountId,
        blockingLevel=data.level,
        reason=data.reason
    )

    db.add(new_entry)
    db.commit()

    return {"message": "Account added to filter"}


@router.delete("/{accountId}")
def remove_filter(accountId: str, db: Session = Depends(get_db)):

    entry = db.query(AccountFilter).filter(
        AccountFilter.accountId == accountId
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(entry)
    db.commit()

    return {"message": "Account is now whitelisted"}