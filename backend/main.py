from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from models import create_db_and_tables, seed_db

app = FastAPI(title="Orbit AI - Matcher")

# ✅ 1. Allow all origins temporarily for debugging (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # temporarily allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 2. Include routers
app.include_router(router, prefix="/api")

# ✅ 3. Handle all OPTIONS preflights manually (safety net)
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

# ✅ 4. Initialize DB
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_db()
