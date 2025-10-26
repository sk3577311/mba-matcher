from pydantic import BaseModel

class MatchRequest(BaseModel):
    gpa: float
    gmat_score: int
    work_experience: int
    program_type: str
