Orbit AI - Right Fit Matcher (SQLite, Windows)

How to run (Windows):

1) Backend
   Open PowerShell or Command Prompt:
     cd orbit-ai\backend
     python -m venv venv
     .\venv\Scripts\activate
     pip install -r requirements.txt
     python seed.py
     uvicorn main:app --reload --port 8000

   Backend will run at: http://localhost:8000
   Test: http://localhost:8000/api/universities

2) Frontend
   Open another terminal:
     cd orbit-ai\frontend
     npm install
     npm run dev

   Frontend at: http://localhost:3000

Quick-run: double-click run_backend.bat and run_frontend.bat (or run them in terminals).

Files included:
- backend/: FastAPI app with SQLite
- frontend/: Next.js 14 App Router frontend (TypeScript + Tailwind)
