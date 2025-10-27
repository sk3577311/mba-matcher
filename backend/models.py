import os
from sqlmodel import SQLModel, Field, create_engine, Session, select

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orbit.db")
engine = create_engine(DATABASE_URL, echo=False)


class University(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    country: str
    avg_gpa: float
    avg_gmat: int
    avg_gre: int
    min_work_exp: int
    acceptance_rate: float  # store as a percentage (e.g., 10 for 10%)
    program_type: str  # "MBA", "MS", etc.


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def seed_db(force_reset: bool = True):
    """Seed the database with 20 universities (MBA + MS)."""
    if force_reset:
        print("🧹 Resetting database...")
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        if session.exec(select(University)).first():
            print("✅ Universities already seeded — skipping.")
            return

        universities = [
            # === MBA Programs ===
            University(name="Harvard Business School", country="USA", avg_gpa=3.8, avg_gmat=730, avg_gre=320, min_work_exp=2, acceptance_rate=10, program_type="MBA"),
            University(name="Stanford GSB", country="USA", avg_gpa=3.8, avg_gmat=733, avg_gre=322, min_work_exp=2, acceptance_rate=9, program_type="MBA"),
            University(name="Wharton School", country="USA", avg_gpa=3.7, avg_gmat=725, avg_gre=321, min_work_exp=2, acceptance_rate=12, program_type="MBA"),
            University(name="INSEAD", country="France", avg_gpa=3.6, avg_gmat=710, avg_gre=315, min_work_exp=3, acceptance_rate=20, program_type="MBA"),
            University(name="London Business School", country="UK", avg_gpa=3.5, avg_gmat=700, avg_gre=310, min_work_exp=3, acceptance_rate=18, program_type="MBA"),
            University(name="MIT Sloan", country="USA", avg_gpa=3.7, avg_gmat=728, avg_gre=320, min_work_exp=2, acceptance_rate=11, program_type="MBA"),
            University(name="Columbia Business School", country="USA", avg_gpa=3.6, avg_gmat=720, avg_gre=318, min_work_exp=2, acceptance_rate=13, program_type="MBA"),
            University(name="Chicago Booth", country="USA", avg_gpa=3.6, avg_gmat=725, avg_gre=319, min_work_exp=2, acceptance_rate=12, program_type="MBA"),
            University(name="Kellogg SOM", country="USA", avg_gpa=3.5, avg_gmat=720, avg_gre=317, min_work_exp=2, acceptance_rate=13, program_type="MBA"),
            University(name="IE Business School", country="Spain", avg_gpa=3.4, avg_gmat=700, avg_gre=310, min_work_exp=3, acceptance_rate=20, program_type="MBA"),

            # === MS Programs ===
            University(name="MIT", country="USA", avg_gpa=3.8, avg_gmat=325, avg_gre=330, min_work_exp=0, acceptance_rate=7, program_type="MS"),
            University(name="Stanford University", country="USA", avg_gpa=3.7, avg_gmat=324, avg_gre=328, min_work_exp=0, acceptance_rate=8, program_type="MS"),
            University(name="UC Berkeley", country="USA", avg_gpa=3.6, avg_gmat=320, avg_gre=325, min_work_exp=0, acceptance_rate=12, program_type="MS"),
            University(name="Carnegie Mellon", country="USA", avg_gpa=3.5, avg_gmat=319, avg_gre=323, min_work_exp=0, acceptance_rate=13, program_type="MS"),
            University(name="University of Cambridge", country="UK", avg_gpa=3.7, avg_gmat=322, avg_gre=327, min_work_exp=0, acceptance_rate=10, program_type="MS"),
            University(name="University of Oxford", country="UK", avg_gpa=3.6, avg_gmat=321, avg_gre=326, min_work_exp=0, acceptance_rate=10, program_type="MS"),
            University(name="ETH Zurich", country="Switzerland", avg_gpa=3.5, avg_gmat=318, avg_gre=322, min_work_exp=0, acceptance_rate=15, program_type="MS"),
            University(name="NUS", country="Singapore", avg_gpa=3.5, avg_gmat=317, avg_gre=320, min_work_exp=0, acceptance_rate=20, program_type="MS"),
            University(name="Tsinghua University", country="China", avg_gpa=3.4, avg_gmat=316, avg_gre=318, min_work_exp=0, acceptance_rate=18, program_type="MS"),
            University(name="University of Toronto", country="Canada", avg_gpa=3.5, avg_gmat=317, avg_gre=320, min_work_exp=0, acceptance_rate=15, program_type="MS"),
        ]

        session.add_all(universities)
        session.commit()
        print("✅ Seeded 20 universities (MBA + MS)")
