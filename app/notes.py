from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from enum import Enum
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note


router=APIRouter(
    tags=["Notas"]
)

class Estado(int, Enum):
    ACTIVO = 1
    INACTIVO = 2
    ELIMINADO = 3

class NoteCreate(BaseModel):
    text:str=Field(...,min_length=3)
    status:Estado = Estado.ACTIVO

class NoteUpdateText(BaseModel):
    text: str = Field(..., min_length=3)



@router.post("/notes")
def create_notes(note: NoteCreate,db:Session=Depends(get_db)):
    new_note=Note(
        text=note.text,
        status=int(note.status)
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.get("/notes")
def list_notes(db:Session=Depends(get_db)):
    return db.query(Note).filter(Note.status !=3 ).all()

@router.get("/notes/{id}")
def list_notes_id(id:int,db:Session=Depends(get_db)):
    note= db.query(Note).filter(Note.id == id ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    return note

@router.delete("/notes/{id}")
def delete_notes(id:int,db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    note.status = 3  # ELIMINADO
    db.commit()

    return {"message": "Nota eliminada", "note": note}

@router.put("/notes/{id}")
def update_notes(id:int,db: Session = Depends(get_db)):
    note=db.query(Note).filter(Note.id==id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    note.status=2
    db.commit()

    return {"message": "Nota desactivada", "note": note}
    
    # for n in notes:
    #     if n["id"] == id:
    #         n["status"]=2
    #         return {"message":"Nota desactivada","note":n}

@router.patch("/notes/{id}")
def update_notas_txt(id:int,data:NoteUpdateText,db: Session = Depends(get_db)):
    note=db.query(Note).filter(Note.id==id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    note.text = data.text
    db.commit()
    return {"message": "Nota actualizada", "note": note}

