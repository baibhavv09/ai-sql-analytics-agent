Docker (ai-sql-analytics-agent/)

Dockerfile — Python 3.12-slim, installs default-libmysqlclient-dev for mysqlclient, non-root appuser, curl-based /health healthcheck, runs uvicorn on :8000.
.dockerignore — excludes .git, .venv, .env, caches, logs, docs, and CI files from the build context.
docker-compose.yml — db (MySQL 8 with volume + healthcheck) and app (built from Dockerfile, waits for db to be healthy, wires DATABASE_URL to db:3306). All configurable via .env.
.env.example — filled in with sensible defaults for the compose stack (DB_HOST=db, DATABASE_URL, APP_PORT, DB_ROOT_PASSWORD, etc.).
GitHub Actions (.github/workflows/)

ci.yml — runs on push/PR to main. Sets up Python 3.12, spins a MySQL 8 service container, installs deps, runs flake8 (with error-only strict check + full stats), black/isort in advisory mode, then pytest if tests/ has any files.
docker-publish.yml — runs on push to main, on v*.*.* tags, or manually. Builds via Buildx with GHA cache, pushes to ghcr.io/<owner>/<repo> tagged with branch, PR, semver, short sha, and latest (main only). Uses the built-in GITHUB_TOKEN, no extra secrets needed.
To run locally:


cp .env.example .env    # fill in SECRET_KEY and OPENAI_API_KEY
docker compose up --build
Heads-up before first push:

The Dockerfile builds from backend/ — CI/lint targets the same path. pyproject.toml says requires-python = ">=3.14" while the image is 3.12 — I'd suggest loosening that to >=3.12 so tooling doesn't complain. Want me to update it?
create_tables.py runs on import of settings and needs a live DB — the Docker build won't run it, but if you want table creation on container start, we should add an entrypoint script.
