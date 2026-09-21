#!/usr/bin/env python
"""Inspect Fanzine and FanzineReview models."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Fanzine, FanzineReview

print("=== Fanzine model ===")
for f in Fanzine._meta.get_fields():
    print(f"  {f.name}: {type(f).__name__}")
    if hasattr(f, 'choices') and f.choices:
        print(f"    choices: {f.choices}")

print("\n=== FanzineReview model ===")
for f in FanzineReview._meta.get_fields():
    print(f"  {f.name}: {type(f).__name__}")
    if hasattr(f, 'choices') and f.choices:
        print(f"    choices: {f.choices}")
