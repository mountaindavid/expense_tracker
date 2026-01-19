from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_pool, init_db, close_pool
from app.routers import expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    init_db()
    try:
        yield
    finally:
        close_pool()


app = FastAPI(lifespan=lifespan)

app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])


@app.get("/")
def read_root():
    return {"message": "Expense Tracker is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
