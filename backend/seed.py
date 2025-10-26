# seed.py
from sqlmodel import Session
from models import engine, University, SQLModel

# Drop existing tables and recreate
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

universities = [
    # MBA Programs
    University(name="Harvard Business School", country="USA", avg_gpa=3.8, avg_gmat=730, avg_gre=320, min_work_exp=2, acceptance_rate=0.1, program_type="MBA"),
    University(name="Stanford Graduate School of Business", country="USA", avg_gpa=3.8, avg_gmat=733, avg_gre=322, min_work_exp=2, acceptance_rate=0.1, program_type="MBA"),
    University(name="Wharton School", country="USA", avg_gpa=3.7, avg_gmat=725, avg_gre=321, min_work_exp=2, acceptance_rate=0.12, program_type="MBA"),
    University(name="INSEAD", country="France", avg_gpa=3.6, avg_gmat=710, avg_gre=315, min_work_exp=3, acceptance_rate=0.2, program_type="MBA"),
    University(name="London Business School", country="UK", avg_gpa=3.5, avg_gmat=700, avg_gre=310, min_work_exp=3, acceptance_rate=0.18, program_type="MBA"),
    University(name="MIT Sloan", country="USA", avg_gpa=3.7, avg_gmat=728, avg_gre=320, min_work_exp=2, acceptance_rate=0.11, program_type="MBA"),
    University(name="Columbia Business School", country="USA", avg_gpa=3.6, avg_gmat=720, avg_gre=318, min_work_exp=2, acceptance_rate=0.13, program_type="MBA"),
    University(name="Chicago Booth", country="USA", avg_gpa=3.6, avg_gmat=725, avg_gre=319, min_work_exp=2, acceptance_rate=0.12, program_type="MBA"),
    University(name="Kellogg School of Management", country="USA", avg_gpa=3.5, avg_gmat=720, avg_gre=317, min_work_exp=2, acceptance_rate=0.13, program_type="MBA"),
    University(name="IE Business School", country="Spain", avg_gpa=3.4, avg_gmat=700, avg_gre=310, min_work_exp=3, acceptance_rate=0.2, program_type="MBA"),

    # MS Programs
    University(name="MIT", country="USA", avg_gpa=3.8, avg_gmat=0, avg_gre=330, min_work_exp=0, acceptance_rate=0.07, program_type="MS"),
    University(name="Stanford University", country="USA", avg_gpa=3.7, avg_gmat=0, avg_gre=328, min_work_exp=0, acceptance_rate=0.08, program_type="MS"),
    University(name="UC Berkeley", country="USA", avg_gpa=3.6, avg_gmat=0, avg_gre=325, min_work_exp=0, acceptance_rate=0.12, program_type="MS"),
    University(name="Carnegie Mellon", country="USA", avg_gpa=3.5, avg_gmat=0, avg_gre=323, min_work_exp=0, acceptance_rate=0.13, program_type="MS"),
    University(name="University of Cambridge", country="UK", avg_gpa=3.7, avg_gmat=0, avg_gre=327, min_work_exp=0, acceptance_rate=0.1, program_type="MS"),
    University(name="University of Oxford", country="UK", avg_gpa=3.6, avg_gmat=0, avg_gre=326, min_work_exp=0, acceptance_rate=0.1, program_type="MS"),
    University(name="ETH Zurich", country="Switzerland", avg_gpa=3.5, avg_gmat=0, avg_gre=322, min_work_exp=0, acceptance_rate=0.15, program_type="MS"),
    University(name="National University of Singapore", country="Singapore", avg_gpa=3.5, avg_gmat=0, avg_gre=320, min_work_exp=0, acceptance_rate=0.2, program_type="MS"),
    University(name="Tsinghua University", country="China", avg_gpa=3.4, avg_gmat=0, avg_gre=318, min_work_exp=0, acceptance_rate=0.18, program_type="MS"),
    University(name="University of Toronto", country="Canada", avg_gpa=3.5, avg_gmat=0, avg_gre=320, min_work_exp=0, acceptance_rate=0.15, program_type="MS"),
]

with Session(engine) as session:
    session.add_all(universities)
    session.commit()

print("✅ Seeded 20 universities (MBA + MS)")
