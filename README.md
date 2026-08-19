# Demotape

Django 5 + HTMX + PostgreSQL + local storage, bootstrapped for local development.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --noinput
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Stack

- Django 6.1
- HTMX 2.0 via `django-htmx`
- PostgreSQL via `psycopg2-binary`
- Local file storage under `media/`; static files under `static/`

## Structure

```
apps/
  core/        # app shell: model, view, template, static
demotape/      # settings, urls, wsgi/asgi
templates/     # project-level templates (optional)
```

## Docs

See `wiki/` for setup notes, local storage plan, and iteration notes.
See Obsidian project note at `~/Documents/Obsidian/Vault/projects/demotape.md`.
