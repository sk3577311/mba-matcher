from fastapi import APIRouter
from sqlmodel import Session, select
from models import University, engine
from schemas import MatchRequest

router = APIRouter()


@router.get("/universities")
def list_universities():
    with Session(engine) as session:
        return session.exec(select(University)).all()


def compute_match_score(req, u):
    """Compute realistic admission probability."""

    # --- Program-based weight configuration ---
    if u.program_type.upper() == "MBA":
        exam_score = req.gmat_score or 0
        avg_exam = u.avg_gmat or 650
        w_exam, w_gpa, w_work = 0.5, 0.3, 0.2
    else:
        exam_score = req.gre_score or 0
        avg_exam = u.avg_gre or 320
        w_exam, w_gpa, w_work = 0.45, 0.45, 0.1

    # --- Exam and GPA ratios ---
    exam_ratio = exam_score / max(avg_exam, 1)
    gpa_ratio = req.gpa / max(u.avg_gpa, 0.01)

    # Normalize to [0.5, 1.2]
    exam_ratio = min(max(exam_ratio, 0.5), 1.2)
    gpa_ratio = min(max(gpa_ratio, 0.5), 1.2)

    # --- Work experience adjustment ---
    if u.min_work_exp > 0:
        work_ratio = min(req.work_experience / u.min_work_exp, 1.0)
    else:
        work_ratio = 1.0 if req.work_experience >= 0 else 0.8

    # --- Base score ---
    raw_score = (exam_ratio * w_exam) + (gpa_ratio * w_gpa) + (work_ratio * w_work)

    # --- Acceptance rate scaling (convert to 0–1 range) ---
    acceptance_factor = u.acceptance_rate / 100
    acceptance_factor = min(max(acceptance_factor, 0.05), 0.6)  # cap extremes

    # --- Final probability ---
    adjusted = raw_score * (0.4 + acceptance_factor)
    probability = round(adjusted * 100, 1)

    # Clamp to realistic range
    probability = max(20.0, min(probability, 95.0))
    return probability


@router.post("/match")
def match_universities(req: MatchRequest):
    with Session(engine) as session:
        unis = session.exec(
            select(University).where(University.program_type == req.program_type)
        ).all()

        if not unis:
            return {"error": "No universities found for this program type"}

        results = []
        for u in unis:
            prob = compute_match_score(req, u)
            results.append({
                "name": u.name,
                "country": u.country,
                "probability": prob,
                "avg_gmat": u.avg_gmat,
                "avg_gpa": u.avg_gpa,
                "acceptance_rate": u.acceptance_rate,
                "program_type": u.program_type,
            })

        results.sort(key=lambda x: x["probability"], reverse=True)
        return results


@router.post("/match/top")
def match_top_university(req: MatchRequest):
    with Session(engine) as session:
        unis = session.exec(
            select(University).where(University.program_type == req.program_type)
        ).all()

        if not unis:
            return {"error": "No universities found"}

        best_uni = max(unis, key=lambda u: compute_match_score(req, u))
        best_score = compute_match_score(req, best_uni)

        return {
            "admission_chance": best_score,
            "program_stats": {
                "acceptance_rate": best_uni.acceptance_rate,
                "avg_gmat": best_uni.avg_gmat,
                "avg_gpa": round(best_uni.avg_gpa, 2),
            },
            "university": best_uni.name,
        }
