from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from models import create_db_and_tables, seed_db

app = FastAPI(title="Orbit AI - Matcher")

# ✅ Allow only trusted frontend origins
origins = [
    "https://mba-matcher.vercel.app/",
]

# ✅ Proper CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """Create DB and seed only once when the app starts."""
    create_db_and_tables()
    seed_db()  # this internally checks if already seeded
