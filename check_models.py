#!/usr/bin/env python
"""Check if Fanzine/FanzineReview models exist and try to add TVOR fanzine with review."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core import models

# Check all models
print("All models in apps.core.models:")
for name in dir(models):
    obj = getattr(models, name)
    if isinstance(obj, type) and hasattr(obj, '_meta'):
        print(f"  {name}")
