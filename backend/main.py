from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from models import create_db_and_tables, seed_db

app = FastAPI(title="Orbit AI - Matcher")

# ✅ Allow frontend domain
origins = [
    "https://mba-matcher-9awl.vercel.app",
    "http://localhost:3000",  # optional for local testing
]

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include router after DB setup
app.include_router(router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """
    Create DB and seed only once when the app starts.
    """
    create_db_and_tables()
    seed_db()   # This internally checks if already seeded
