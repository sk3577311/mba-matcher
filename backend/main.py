from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from models import create_db_and_tables

app = FastAPI(title="Orbit AI - Matcher")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
