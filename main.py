from fastapi import FastAPI
from sqlalchemy import text
from database.db import get_db
from database.db import get_db, engine, Base
from models.account import Account   # IMPORTANT: Must import model
from router.acc_router import router as account_router
from router.transaction_router import router as transaction_router

app = FastAPI()

# 🔹 Create tables
Base.metadata.create_all(bind=engine)

# 🔹 Include Account Router
app.include_router(account_router)
app.include_router(transaction_router)


@app.on_event("startup")
def test_db_connection():
    try:
        db_generator = get_db()
        db = next(db_generator)

        db.execute(text("SELECT 1"))

        print("✅ Database Connected Successfully")

    except Exception as e:
        print("❌ Database Connection Failed")
        print(e)

    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Bank Server Running"}
