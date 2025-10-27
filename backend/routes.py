from fastapi import APIRouter
from sqlmodel import Session, select
from models import University, engine
from schemas import MatchRequest

router = APIRouter()

# -------------------------------------------------------------------
# 📘 List all universities (for debugging or dropdown display)
# -------------------------------------------------------------------
@router.get("/universities")
def list_universities():
    """Return all universities in the database"""
    with Session(engine) as session:
        universities = session.exec(select(University)).all()
        return universities


# -------------------------------------------------------------------
# 🎯 Match all universities ranked by probability
# -------------------------------------------------------------------
@router.post("/match")
def match_universities(req: MatchRequest):
    """Return a ranked list of universities based on admission probability"""
    with Session(engine) as session:
        unis = session.exec(
            select(University).where(University.program_type == req.program_type)
        ).all()

        results = []
        for u in unis:
            gmat_ratio = req.gmat_score / max(u.avg_gmat, 1)
            gpa_ratio = req.gpa / max(u.avg_gpa, 0.01)
            work_bonus = min(req.work_experience / max(u.min_work_exp, 1), 1.0)
            acceptance_factor = 1 - u.acceptance_rate

            # Weighted scoring formula
            score = (
                gmat_ratio * 0.4 +
                gpa_ratio * 0.4 +
                work_bonus * 0.1 +
                acceptance_factor * 0.1
            )
            score = max(0.0, min(score, 1.0))  # clamp between 0–1

            results.append({
                "name": u.name,
                "country": u.country,
                "probability": round(score * 100, 1),
                "avg_gmat": u.avg_gmat,
                "avg_gpa": u.avg_gpa,
                "acceptance_rate": round(u.acceptance_rate * 100, 1),
                "program_type": u.program_type,
            })

        results.sort(key=lambda x: x["probability"], reverse=True)
        return results


# -------------------------------------------------------------------
# 🏆 Match top (best-fit) university
# -------------------------------------------------------------------
@router.post("/match/top")
def match_top_university(req: MatchRequest):
    """Return only the single best-fit university"""
    with Session(engine) as session:
        unis = session.exec(
            select(University).where(University.program_type == req.program_type)
        ).all()

        best_uni = None
        best_score = -1

        for u in unis:
            gmat_ratio = req.gmat_score / max(u.avg_gmat, 1)
            gpa_ratio = req.gpa / max(u.avg_gpa, 0.01)
            work_bonus = min(req.work_experience / max(u.min_work_exp, 1), 1.0)
            acceptance_factor = 1 - u.acceptance_rate

            score = (
                gmat_ratio * 0.4 +
                gpa_ratio * 0.4 +
                work_bonus * 0.1 +
                acceptance_factor * 0.1
            )
            score = max(0.0, min(score, 1.0))

            if score > best_score:
                best_score = score
                best_uni = u

        if not best_uni:
            return {"error": "No universities found"}

        return {
            "admission_chance": round(best_score * 100, 1),
            "program_stats": {
                "acceptance_rate": round(best_uni.acceptance_rate * 100, 1),
                "avg_gmat": best_uni.avg_gmat,
                "avg_gpa": round(best_uni.avg_gpa, 2),
            },
            "university": best_uni.name,
        }
