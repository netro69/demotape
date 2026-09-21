# Demotape — Project Context

## Stack
- Django 6.1 + HTMX 2.0 + PostgreSQL
- Python 3.12
- Local file storage under `media/`, static under `static/`

## Before ANY Work — READ THESE
1. `~/Projects/demotape/README.md` — This file (stack + quick start)
2. `~/Projects/demotape/wiki/` — Setup notes, iteration log, local storage plan
3. `~/Documents/Obsidian/Vault/projects/demotape.md` — Obsidian project note
4. `~/Documents/Obsidian/Vault/projects/demotape-research-log.md` — Research findings
5. `~/Documents/Obsidian/Vault/projects/demotape-qa-log.md` — QA issues + fixes
6. `~/Documents/Obsidian/Vault/Research/bbs-scene-research.md` — BBS research methodology
7. `~/Documents/Obsidian/Vault/_memory-spine.md` — Memory architecture
8. `~/Documents/Obsidian/Vault/_index.md` — Vault schema (where files go)

## Project Structure
```
demotape/
├── apps/core/         # Django app: models, views, templates
├── demotape/          # Settings, URLs, WSGI/ASGI
├── wiki/              # Setup, iteration log, local storage docs
├── research/          # Researcher output (.md + .json)
├── data/              # Structured research data (JSON)
├── research_output/   # Processed research links
├── templates/         # Project-level templates
├── manage.py
└── *.py               # Utility scripts (research, QA, fixes)
```

## Research Methodology
- Crawl band-to-band via forums (RadioChitarra, DeBaser)
- Find YouTube videos in comments
- Document connections (member_of, influenced_by, collaborated_with)
- Log findings in `research/` and `data/`

## QA Pipeline
- `qa_checker.py` runs every 30 min via cron
- Checks: duplicate URLs, self-references, invalid enums, malformed URLs, orphaned FKs, dead links
- Issues logged to `~/Documents/Obsidian/Vault/projects/demotape-qa-log.md`
- Fix loop: Fisherman adds → QA validates → Issues clustered → Agent fixes → QA re-checks

## Knowledge Sharing Protocol
- **Read first.** Check wiki, Obsidian, and session history before researching.
- **Write back.** Research findings → `research/` + `data/`. QA issues → Obsidian log.
- **Query before research.** Search Obsidian and existing research before opening browser.

## File Lifecycle
- Temp files → `/tmp/` (cleaned by cron hourly)
- Research files → `research/` or `data/` (project schema)
- Knowledge docs → `wiki/` (project) or `~/Documents/Obsidian/Vault/` (cross-project)
- NEVER create files at `~/` or `~/Documents/` root.

## Memory Rules
- `memory` tool = pointer to Obsidian (max 2200 chars).
- Obsidian Vault = storage of truth.
- Never duplicate Vault content into memory — point to it.

## Task Brief Requirement
Every task MUST include:
1. **Relevant context** — pointers to wiki/Obsidian files
2. **Lessons learned** — past failures on this topic
3. **Expected output** — where to write results

## After EVERY Task — Log:
- What worked → `~/Documents/Obsidian/Vault/LLM-wiki/topics/lessons-learned.md`
- What failed → `~/Documents/Obsidian/Vault/LLM-wiki/topics/pitfalls.md`
- New research → `research/` or `data/`
- New files → verify they're in the correct project location

## FILE HEADER CONVENTION
Every new file MUST include a header:
- Python: `# Created-by: <profile> | Date: YYYY-MM-DD`
- Markdown: `<!-- created-by: <profile> | date: YYYY-MM-DD -->`
- JSON: Add `"created-by": "<profile>", "date": "YYYY-MM-DD"` at top level.

This enables the audit cron to verify accountability and track orphaned files.

## Research Gate
Before starting ANY task:
1. Check `wiki/` for existing project docs
2. Search `~/Documents/Obsidian/Vault/LLM-wiki/topics/shared-lessons.md` for related topics
3. Search `~/Documents/Obsidian/Vault/LLM-wiki/topics/pitfalls.md` for known mistakes
4. Search `~/Documents/Obsidian/Vault/` for related topics
5. Search `session_search` for past attempts
6. Only THEN begin work

## Common Pitfalls
- Schema drift: `link_type` values changed over time (check models.py before assuming)
- Duplicate research: Fisherman may re-crawl existing bands — check first
- QA false positives: dead link spot-checks can fail for temporary reasons — verify before fixing
- PostgreSQL must be running: `sudo systemctl start postgresql` if connection refused
