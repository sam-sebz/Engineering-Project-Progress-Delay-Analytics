# TRD

## Architecture
Browser -> FastAPI -> validation -> project/activity service -> ML risk model -> SQLite -> dashboard.

## Stack
Python, FastAPI, pandas, scikit-learn, SQLite, HTML, CSS and JavaScript.

## API
GET /api/health
GET /api/metrics
GET /api/projects
POST /api/projects
POST /api/projects/{id}/activities
PUT /api/activities/{id}/progress
POST /api/activities/{id}/delay-risk
