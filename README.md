# AI-Powered Environmental Intelligence System

A full-stack web app that shows real-time air quality (AQI), weather and traffic
for the user's location, and later predicts AQI and recommends cleaner travel routes.

## Tech Stack

- Frontend: React, TypeScript, Vite, Leaflet.js
- Backend: Python, FastAPI
- Database: InfluxDB (runs in Docker)
- External APIs: OpenAQ, WAQI, OpenWeatherMap

## Project Structure

```
aqi-intelligence-system/
├── frontend/     React app
├── backend/      FastAPI server
└── README.md
```

## How to Run

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000 (API docs at /docs).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173.

### Database

```bash
docker run -d --name influxdb -p 8086:8086 influxdb:2.7
```

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in your keys.
Copy `frontend/.env.example` to `frontend/.env`.

## Status

Milestone 1 (Weeks 1-2): in progress
