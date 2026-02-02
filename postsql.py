from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, ConfigDict

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
class EmployeeCreate(BaseModel):
    name: str
    age: int
    

class EmployeeRead(BaseModel):
    id: int
    name: str
    age: int
    model_config = ConfigDict(from_attributes=True)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message":"Employees"}

@app.post("/employee/", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(name=employee.name, age=employee.age)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
@app.get("/employees/", response_model=list[EmployeeRead])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees
