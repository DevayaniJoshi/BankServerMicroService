from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.db import get_db
from sqlalchemy import text

app = FastAPI()

@app.post("/user/{username}/photo/{photoId}")
def root(username:str,photoId:int,size:int,type:str="jpeg"):
    
    return {f"message":f"The user name is {username} , the id is {photoId}, the {size}, and {type}"}




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

