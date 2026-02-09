from sqlalchemy import Column,Integer,String
from app.database import Base

class Note(Base):
    __tablename__="notes"

    id=Column(Integer,primary_key=True,index=True)
    text=Column(String,nullable=False)
    status=Column(Integer,nullable=False, default=1)



