from fastapi import FastAPI
from app.notes import router as notes_router
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)


app=FastAPI(
    title="Api notas"
)

@app.get("/")
def root():
    return {"status":"ok"}

app.include_router(notes_router)