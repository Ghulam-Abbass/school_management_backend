from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from sqlalchemy import text 

app = FastAPI()

@app.get("/check-db")
async def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Run a simple SQL query to check the connection using text() function
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Test client
from fastapi.testclient import TestClient

client = TestClient(app)

# Test client
from fastapi.testclient import TestClient

client = TestClient(app)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}