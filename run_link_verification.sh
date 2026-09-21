#!/bin/bash
# Created-by: forge | Date: 2026-09-21
# Wrapper for link_verifier.py — called by qa_checker or cron

set -e
cd ~/Projects/demotape
source .venv/bin/activate 2>/dev/null || true
python link_verifier.py --limit 50 2>&1
echo "Exit code: $?"
