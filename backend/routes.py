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
    """Compute realistic admission probability safely for both MBA and MS."""

    # --- Determine exam type ---
    program = u.program_type.upper()

    # Handle missing exam scores safely
    gmat = req.gmat_score if hasattr(req, "gmat_score") and req.gmat_score else 0
    gre = req.gre_score if hasattr(req, "gre_score") and req.gre_score else 0
    gpa = req.gpa if hasattr(req, "gpa") else 0
    work_exp = req.work_experience if hasattr(req, "work_experience") else 0

    # --- MBA vs MS weighting ---
    if program == "MBA":
        exam_score = gmat or (gre * 0.214 + 200)  # convert GRE→GMAT equivalent if GRE used
        avg_exam = u.avg_gmat or 650
        w_exam, w_gpa, w_work = 0.5, 0.3, 0.2
    else:  # MS or others
        exam_score = gre or (gmat * 3.1 - 620)  # convert GMAT→GRE if GMAT used
        avg_exam = u.avg_gre or 320
        w_exam, w_gpa, w_work = 0.45, 0.45, 0.1

    # --- Normalize values ---
    exam_ratio = exam_score / max(avg_exam, 1)
    gpa_ratio = gpa / max(u.avg_gpa, 0.01)

    # Clamp ratios
    exam_ratio = min(max(exam_ratio, 0.4), 1.2)
    gpa_ratio = min(max(gpa_ratio, 0.4), 1.2)

    # --- Work experience adjustment ---
    work_ratio = 1.0
    if u.min_work_exp and u.min_work_exp > 0:
        work_ratio = min(work_exp / u.min_work_exp, 1.0)

    # --- Acceptance rate scaling ---
    acc_factor = u.acceptance_rate / 100.0
    acc_factor = min(max(acc_factor, 0.05), 0.6)

    # --- Weighted score ---
    raw_score = (exam_ratio * w_exam) + (gpa_ratio * w_gpa) + (work_ratio * w_work)
    adjusted = raw_score * (0.4 + acc_factor)

    # --- Final Probability ---
    probability = round(adjusted * 100, 1)
    probability = max(20.0, min(probability, 95.0))

    return probability


@router.post("/match")
def match_universities(req: MatchRequest):
    """Return ranked universities with realistic admission chances."""
    with Session(engine) as session:
        unis = session.exec(
            select(University).where(University.program_type == req.program_type)
        ).all()

        if not unis:
            return {"error": "No universities found for this program type"}

        results = []
        for u in unis:
            try:
                prob = compute_match_score(req, u)
            except Exception as e:
                print(f"⚠️ Error computing score for {u.name}: {e}")
                prob = 50.0  # fallback value

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
    """Return the single best-fit university."""
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
