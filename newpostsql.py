from fastapi import FastAPI,Depends
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, ConfigDict
from typing import List

DATABASE_URL= "postgresql+psycopg2://postgres:postgres123@localhost:5432/fastapi_db"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base=declarative_base()

class People(Base):
    __tablename__="people"
    vote_id=Column(Integer,primary_key=True, index=True)
    p_name=Column(String)
    p_age=Column(Integer)
    p_f_name=Column(String)
    phn_no=Column(Integer)
    voter_eligible=Column(Boolean, default=False)

class CreatePeople(BaseModel):
        p_name:str
        p_age:int
        p_f_name:str
        phn_no:int
class ResponsePeople(CreatePeople):
        class Config:
            model_config=ConfigDict(from_attributes=True)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@app.get("/people")
def make():
    return {"message":"People voter list"}

@app.post("/people/create",response_model=List[ResponsePeople])
def create(people: List[CreatePeople], db:Session = Depends(get_db)):
    new_people=[]
    
    for person in people:
      new_person=People(**person.model_dump())
      db.add(new_person)
      new_people.append(new_person)
    db.commit()
   
    for p in new_people:
     db.refresh(p)
    
    return new_people

@app.put("/people/update")
def update_list(age_limit:int=18,db:Session=Depends(get_db)):
    not_elligible=(db.query(People).filter(People.p_age<age_limit).update({People.voter_eligible:False},synchronize_session=False))

    eligible=(db.query(People).filter(People.p_age>=age_limit).update({People.voter_eligible:True},synchronize_session=False))
    
    db.commit()
    
    return{"age_limit":age_limit,
           "eligible_voter_updated":"eligible",
           "not_eligible_updated":"not_eligible"}






