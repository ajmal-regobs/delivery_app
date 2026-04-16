# Delivery App

FastAPI + PostgreSQL app to add, remove, and list deliveries. Includes a simple HTML UI and a JSON REST API.

## Stack

- **FastAPI** — web framework
- **SQLAlchemy 2.0** — ORM (`Delivery` table auto-created on startup)
- **PostgreSQL** — provisioned via DevLift (`delivery-app-pg`)
- **Jinja2** — HTML UI templates

## Setup

1. Create a virtualenv and install deps:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Postgres credentials
   (DevLift exposes them as the discrete `POSTGRES_*` env vars listed there).

3. Run the app:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open http://localhost:8000 for the UI, or http://localhost:8000/docs for the OpenAPI spec.

## REST API

| Method | Path                      | Description             |
|--------|---------------------------|-------------------------|
| GET    | `/deliveries`             | List all deliveries     |
| POST   | `/deliveries`             | Add a delivery (JSON)   |
| DELETE | `/deliveries/{id}`        | Remove a delivery       |

Add delivery payload:

```json
{
  "recipient": "Alice",
  "address": "123 Main St",
  "item": "Book",
  "status": "pending"
}
```

## UI routes

- `GET /` — list + add form
- `POST /ui/deliveries` — add via form submit
- `POST /ui/deliveries/{id}/delete` — remove via form submit
