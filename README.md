# UptimeGuard

UptimeGuard is a lightweight uptime monitoring service built with FastAPI and PostgreSQL. It exposes a simple web UI and REST API for adding URLs to monitor, while a background worker periodically checks each site and stores results in the database.

## Features

- Add websites to monitor via web UI or REST API
- Periodic uptime checks with configurable intervals
- Stores site metadata and check results in PostgreSQL

## Architecture

- `app.api.main` — FastAPI web application and REST API
- `app.worker.checker` — background worker that checks registered sites
- `app.db.init_db` — initializes PostgreSQL and database tables
- `app.db.models` — SQLAlchemy models for monitored sites and check results
- `app.cfg.config` — environment-driven configuration
- `app.static` — simple frontend for submitting URLs and check interval

## Requirements

- Docker
- Docker Compose

## Getting Started

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Update `.env` with your PostgreSQL settings:

```dotenv
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<your-db-name>
```

3. Start the application stack:

```bash
docker-compose up --build
```

4. Open the app in your browser:

- UI and API root: `http://localhost:8000`

## API Endpoints

- `GET /` — serves the web UI from `app/static/index.html`
- `POST /site` — add a site to monitor
  - Request body:
    ```json
    {
      "url": "https://example.com",
      "interval_minutes": 5
    }
    ```
- `GET /sites` — list monitored site URLs

## Local Development

If you want to run the app without Docker, activate your Python environment and install dependencies from `requirements.txt`.

```bash
source UptimeGuard/bin/activate
pip install -r requirements.txt
```

Then run the API server directly:

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

And run the worker in a separate shell:

```bash
python -m app.worker.checker
```

## Notes

- The worker polls every 10 seconds and performs checks only when a site's configured interval has elapsed.
- Site URLs are normalized to use `https://` when no scheme is provided.

## License

This project includes a `LICENSE` file in the repository.
