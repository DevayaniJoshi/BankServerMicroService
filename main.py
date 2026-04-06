from fastapi import FastAPI
from sqlalchemy import text
from database.db import get_db, engine, Base
from models.account import Account   # IMPORTANT: Must import model
from models.account_filter import AccountFilter

from router.acc_router import router as account_router
from router.transaction_router import router as transaction_router
from router.filter_router import router as filter_router

# 🔥 CACHE IMPORTS
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # 🔥 In-Memory Cache (instead of Redis)
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    print("✅ In-Memory Cache Initialized")

    yield

app = FastAPI(lifespan=lifespan)

# 🔹 Create tables
Base.metadata.create_all(bind=engine)

# 🔹 Include Routers
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(filter_router)


# 🔥 STARTUP EVENT (MERGED PROPERLY)
@app.on_event("startup")
async def startup():
    # ✅ Initialize Cache
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    # ✅ Test DB Connection
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


# 🔹 Home Route
@app.get("/")
def home():
    return {"message": "Bank Server Running"}