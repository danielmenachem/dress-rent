from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.models import dress, customer, rental
from backend.database import get_db
from backend.services.dress_service import get_dresses

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Dress Rental API is running!"}

@app.get("/dresses")
def list_dresses(session: Session = Depends(get_db)):
    dresses = get_dresses(session)
    return dresses