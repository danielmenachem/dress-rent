from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.models import dress, customer, rental
from backend.database import get_db
from backend.services.dress_service import get_dresses, get_dress, add_dress, update_dress
from backend.schemas.dress import DressResponse, DressCreate, DressUpdate

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Dress Rental API is running!"}

@app.get("/dresses", response_model=list[DressResponse])
def list_dresses(session: Session = Depends(get_db)):
    dresses = get_dresses(session)
    return dresses

@app.get("/dresses/{dress_id}", response_model=DressResponse)
def read_dress(dress_id: int, session: Session = Depends(get_db)):
    try:
        dress = get_dress(session, dress_id)
        return dress
    except ValueError:
        raise HTTPException(
            status_code=404, 
            detail="Dress not found"
        )
    
@app.post("/dresses", response_model=DressResponse, status_code=201)
def create_dress(dress: DressCreate, session: Session = Depends(get_db)):
    new_dress = add_dress(
        session,
        designer=dress.designer,
        color=dress.color,
        size=dress.size,
        price=dress.price,
        image_path=dress.image_path
    )
    return new_dress

@app.patch("/dresses/{dress_id}", response_model=DressResponse)
def patch_dress(
    dress_id: int,
    dress_update: DressUpdate,
    session: Session = Depends(get_db)
):
    updates = dress_update.model_dump(exclude_none=True)

    try:
        updated_dress = update_dress(
            session,
            dress_id=dress_id,
            **updates
        )
        return updated_dress
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))