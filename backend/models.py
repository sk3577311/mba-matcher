import os
from sqlmodel import SQLModel, Field, create_engine

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orbit.db")
engine = create_engine(DATABASE_URL, echo=False)

class University(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    country: str  # Add this
    avg_gpa: float
    avg_gmat: int
    avg_gre: int
    min_work_exp: int
    acceptance_rate: float  # 0.0-1.0
    program_type: str  # "MBA", "MS", etc.

    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
