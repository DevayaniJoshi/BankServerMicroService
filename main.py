from fastapi import FastAPI
from sqlalchemy import text
from database.db import get_db
from database.db import get_db, engine, Base
from models.account import Account   # IMPORTANT: Must import model
from router.acc_router import router as account_router


app = FastAPI()

# 🔹 Create tables
Base.metadata.create_all(bind=engine)

# 🔹 Include Account Router
app.include_router(account_router)


@app.post("/user/{username}/photo/{photoId}")
def user_photo(username: str, photoId: int, size: int, type: str = "jpeg"):
    return {
        "message": f"The user name is {username}, the id is {photoId}, the size is {size}, and type is {type}"
    }


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
