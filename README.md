# Hackerz - Hospital Emergency Management API

Production-ready Flask backend with:
- PostgreSQL
- SQLAlchemy ORM
- JWT authentication
- Doctor, Patient, and Alert models
- Blueprint-based routing structure

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/hackerz"
export JWT_SECRET_KEY="super-secret-key"
export API_USERNAME="admin"
export API_PASSWORD="admin123"
```

## Run

```bash
python app.py
```

## Auth

### `POST /auth/login`
Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "<jwt-token>"
}
```

Use token as:

```http
Authorization: Bearer <jwt-token>
```

## Routes

- `POST /doctors`
- `GET /doctors`
- `PUT /doctors/<id>`
- `POST /patients`
- `GET /patients-summary`
- `GET /alerts`

## Alert logic

An alert is created when:

- emergency patients > 15
- available doctors < 2
