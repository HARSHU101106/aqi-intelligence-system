from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users          # NEW

app = FastAPI(title="AQI Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)       # NEW

@app.get("/health")
def health():
    return {"status": "ok"}