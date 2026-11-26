# Release Tracker

A portfolio starter for tracking release readiness and deployment tasks using FastAPI, SQLite and a browser interface.

## Run locally

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and /docs for API documentation.

## Architecture

Browser → FastAPI REST API → SQLite. GitHub Actions runs tests and builds a Docker image on push and pull request.

## Docker

```bash
docker build -t release-tracker:v1 .
docker run --rm -p 127.0.0.1:8000:8000 -v release-data:/data release-tracker:v1
```

## AI-assisted development exercise

Use Claude Code on a feature branch to implement task filtering, then use Codex to review the diff and propose tests. Review changes manually, run tests and open a pull request. See CLAUDE.md and AGENTS.md. Actual use of these tools is pending.

## Deployment and rollback

Use separate ports and volumes for development and staging. Keep known-good image tags and back up data before schema changes. Roll back by restarting the previous compatible image and checking /health and CRUD operations. Production deployment is not configured. This starter has no authentication and should not be publicly exposed.
