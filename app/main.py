from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Expense Tracker is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}