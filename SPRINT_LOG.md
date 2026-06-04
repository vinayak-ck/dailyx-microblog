# DailyX Sprint Log

## Sprint 1 — Security & Deployment Hardening
**Date:** June 2026  
**Status:** ✅ Complete

### Changes made

#### 1. `.gitignore` (new file)
- Excludes `db.sqlite3` from git (was publicly visible on GitHub)
- Excludes `.env` (secret key protection)
- Excludes `staticfiles/`, `__pycache__/`, `.DS_Store`, IDE files
- Excludes `portfolio1.png` (large stray image in repo root)

#### 2. `.env.example` (new file)
- Template showing what env vars are needed
- Safe to commit — no real secrets, just keys with placeholder values
- New devs copy this to `.env` to get started

#### 3. `dailyx/settings.py` (updated)
- `ALLOWED_HOSTS`: no longer `['*']` — reads `RENDER_EXTERNAL_HOSTNAME` env var (set automatically by Render)
- `conn_max_age=600` added to `dj_database_url.parse()` — keeps DB connections alive, reduces latency
- Added security headers: `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = "DENY"`
- Organised with clear section comments

#### 4. `Procfile` (updated)
- Was: `web: gunicorn dailyx.wsgi:application` (1 worker, blocks on slow queries)
- Now: `--workers 2 --threads 2 --timeout 30 --log-level info`
- 2 workers × 2 threads = handles 4 concurrent requests without stalling

#### 5. `manage.py` (updated)
- Calls `load_dotenv()` on startup so `.env` is loaded in local dev automatically

#### 6. `templates/404.html` + `templates/500.html` (new)
- Branded error pages matching DailyX style
- Shown automatically when `DEBUG=False` (which is now the production default)

### What you need to do on Render
1. Go to Render dashboard → your web service → **Environment**
2. Add these env vars:
   - `SECRET_KEY` → generate with: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `DEBUG` → `False`
   - `RENDER_EXTERNAL_HOSTNAME` → `dailyx-microblog.onrender.com`
3. Redeploy

### After this sprint — git commands to run
```bash
git rm --cached db.sqlite3          # remove sqlite from git tracking
git rm --cached portfolio1.png      # remove stray image
git add .gitignore .env.example dailyx/settings.py Procfile manage.py templates/404.html templates/500.html SPRINT_LOG.md
git commit -m "Sprint 1: security hardening, .gitignore, error pages, gunicorn fix"
git push
```

---

## Sprint 2 — Cold Start Fix (Planned)
- Keep-alive cron job setup
- Render configuration guide

## Sprint 3 — Database Backup & Migration (Planned)
- pg_dump backup script
- Supabase migration guide (if staying on free tier)

## Sprint 4 — Rate Limiting (Planned)
- django-ratelimit on post creation view
- Spam protection

## Sprint 5 — Upgrade Features (Planned)
- Dark mode toggle
- Personalised feed (follows only)
- Trending section
