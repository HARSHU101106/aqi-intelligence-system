# AI-Powered Environmental Intelligence System

A full-stack web app that shows real-time air quality (AQI), weather and traffic
for the user's location, and later predicts AQI and recommends cleaner travel routes.

Built as part of the Infosys Springboard Internship.

## Features (Milestone 1)

- Browser location capture with user consent and error handling
- Real-time AQI and pollutants (PM2.5, PM10, NO2, O3, CO) from WAQI and OpenAQ
- Weather data from OpenWeatherMap
- Traffic information (where provider access is available)
- User registration with health sensitivity profile (asthma, elderly, children)
- Historical environmental data stored in InfluxDB
- Dashboard with AQI card, pollutant grid, weather card and interactive Leaflet map

## Tech Stack

- Frontend: React, TypeScript, Vite, Leaflet.js
- Backend: Python, FastAPI
- Database: InfluxDB (runs in Docker)
- External APIs: OpenAQ, WAQI, OpenWeatherMap, TomTom

## Prerequisites

Node.js (LTS), Python 3.11+, Git, Docker Desktop

## Project Structure

```
aqi-intelligence-system/
├── frontend/          React app
│   └── src/           api, components, hooks, types, utils
├── backend/           FastAPI server
│   └── app/           core, db, routers, schemas, services
├── docs/              Technical documentation and screenshots
└── README.md
```

## How to Run

### 1. Database

```bash
docker run -d --name influxdb -p 8086:8086 influxdb:2.7
```

Open http://localhost:8086, create an organization and a bucket named
`environment_data`, then copy the API token.

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate    # Git Bash. In PowerShell use: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your keys
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000 (API docs at /docs).

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at http://localhost:5173.

## Environment Variables

Backend (`backend/.env`):

| Variable                                            | Purpose             |
| --------------------------------------------------- | ------------------- |
| INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET | InfluxDB connection |
| OPENAQ_API_KEY                                      | OpenAQ access       |
| WAQI_TOKEN                                          | WAQI access         |
| OPENWEATHER_API_KEY                                 | Weather data        |
| TOMTOM_API_KEY                                      | Traffic data        |

Frontend (`frontend/.env`):

| Variable     | Purpose                             |
| ------------ | ----------------------------------- |
| VITE_API_URL | Backend URL (http://localhost:8000) |

## API Endpoints

| Method | Endpoint       | Description                       |
| ------ | -------------- | --------------------------------- |
| GET    | /health        | Server health check               |
| GET    | /health/db     | Database connection check         |
| POST   | /users         | Create user profile               |
| GET    | /users/{email} | Get user profile                  |
| POST   | /location      | Validate and process coordinates  |
| GET    | /air-quality   | AQI and pollutants for a location |
| GET    | /environment   | Combined AQI, weather and traffic |

Full details are in `docs/TECHNICAL_DOCUMENTATION.md`.

## Screenshots

![Dashboard](docs/screenshots/dashboard.png)
![Map](docs/screenshots/map.png)

## Running Tests

```bash
cd backend
pytest
```

## Known Limitations

- Some stations do not report every pollutant
- Traffic data depends on provider access
- Nearest monitoring station may be far from the user
- No login system yet
- Forecasting, route advisory and push notifications come in later milestones

## Status

- Milestone 1 (Weeks 1-2): Complete
- Milestone 2 (Weeks 3-4): Predictive AQI forecasting, not started
