**Purpose**: Quick orientation for AI coding agents working on this repository. Focus on runtime, template patterns, imports, and environment-driven behavior so changes are correct and safe.

- **Big picture**: The project is a small Flask service in `api/` that renders an SVG (or HTML template) representing a Spotify "now playing" or recently-played item. It loads templates from `api/templates.json` and Jinja2 files in `api/templates/`, fetches data from the Spotify Web API, and produces a response used for README widgets.

- **Key files**:
  - `api/spotify.py`: single largest implementation file; contains Flask app, token refresh logic, HTTP helpers (`get`, `refreshToken`), SVG/template generation (`makeSVG`, `barGen`, `gradientGen`). Primary place to make API or template changes.
  - `api/index.py`: Vercel entrypoint that imports `app` from `spotify.py`. Required for Vercel deployments.
  - `api/templates.json` and `api/templates/*.j2`: theme selection and template sources. `templates.json` keys: `current-theme` and a `templates` map (e.g., `dark -> spotify-dark.html.j2`).
  - `requirements.txt`: lists runtime dependencies (Flask, requests, python-dotenv, colorthief). Use this to avoid adding incompatible libs.
  - `Dockerfile`, `docker-compose.yml`, `Procfile`, `app.json`, `vercel.json`: deployment/runtime entry points. Note Dockerfile `WORKDIR /api` and `CMD ["gunicorn", "--workers=1", "--bind", "0.0.0.0:5000", "spotify:app"]` — imports assume module name `spotify` when running in `/api`.

- **Runtime & dev workflows** (examples):
  - Local dev (quick): create `.env` with `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, `SPOTIFY_REFRESH_TOKEN`, then run:
    - `python api/spotify.py` (uses Flask dev server; `debug=True` in `__main__`)
  - Production-like (gunicorn):
    - From repo root (module path matters): `gunicorn --workers=1 api.spotify:app` (used by `app.json`/Heroku)
    - Inside Docker context (image `WORKDIR /api`): `gunicorn --workers=1 spotify:app` (Dockerfile uses this form because files are copied into `/api`).
  - Docker: `docker-compose up --build` (see `docker-compose.yml` binding `./api:/api` which preserves local changes inside the container).
  - Vercel: Uses `api/index.py` as entrypoint (imports `app` from `spotify.py`). Set env vars in Vercel dashboard. `vercel.json` routes all traffic to `api/index.py`.

- **Environment variables & secrets**:
  - Required: `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, `SPOTIFY_REFRESH_TOKEN`. The code uses `python-dotenv` to load `.env` files when present.
  - The app exchanges `SPOTIFY_REFRESH_TOKEN` for an access token at `https://accounts.spotify.com/api/token`. Keep refresh token secure.

- **Import / path notes**: Because the container `WORKDIR` is `/api`, the Docker CMD uses `spotify:app`. Outside Docker (repo root), code expects `api.spotify` for gunicorn. When editing imports or running tests, be mindful of the working directory used to run Python.

- **Template & UI patterns**:
  - `api/templates.json` controls the template name returned by `getTemplate()` in `api/spotify.py`. Change the Jinja templates in `api/templates/` when adjusting markup or inlined CSS.
  - `makeSVG()` passes `image` as a base64 string and color palettes from `colorthief.get_palette()` to templates. Templates expect variables like `contentBar`, `barCSS`, `artistName`, `songName`, `image`, `barPalette`, `songPalette`.

- **Error handling & retries**:
  - `get()` refreshes the token on HTTP 401 by calling `refreshToken()` and retries once. It raises on 204 (no content). Code prints JSON on token errors — be cautious when changing logging to avoid leaking secrets.

- **Code style & linting**:
  - `requirements.txt` includes `autopep8` and `pycodestyle` — the project expects PEP8 formatting. Run `autopep8 --in-place --aggressive <file>` before committing changes if adjusting formatting.

- **When editing `api/spotify.py`**:
  - Prefer minimal, focused changes. This file mixes HTTP, templating, and SVG-generation logic in one place — avoid large refactors without tests. If you split logic, keep runtime import compatibility in mind (module path differences described above) and update Dockerfile/Procfile if the app import path changes.
  - If adding new templates, update `api/templates.json` and include the `.j2` file in `api/templates/`.

- **Tests & CI**: No tests or CI configuration found. When adding behavior-critical changes (auth, token flow, network retries), test locally with valid Spotify creds and try the `docker-compose` route to approximate production.

- **Performance / caching**:
  - Responses set header `Cache-Control: s-maxage=1`. Template generation can be CPU-heavy (image download + palette extraction). Consider adding local caching for album art or palette results if you change `gradientGen`.

- **Examples of quick edits**:
  - Change default theme: edit `api/templates.json` -> `"current-theme": "light"`.
  - Adjust gunicorn command for local container debugging: update `Dockerfile` `CMD` or run container with `COMMAND` override.

If something in these instructions is unclear or you'd like more detail (tests, CI, or a suggested refactor plan), tell me which area to expand. After feedback I'll iterate on this file.
