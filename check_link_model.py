#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Link

# Check valid link types
print("Link model fields:")
for f in Link._meta.get_fields():
    print(f"  {f.name}: {type(f).__name__}")
    
# Check link_type choices if available
if hasattr(Link, 'LINK_TYPE_CHOICES'):
    print("\nLINK_TYPE_CHOICES:")
    for k, v in Link.LINK_TYPE_CHOICES:
        print(f"  {k}: {v}")
elif hasattr(Link, 'link_type'):
    field = Link._meta.get_field('link_type')
    if hasattr(field, 'choices'):
        print("\nlink_type choices:")
        for k, v in field.choices:
            print(f"  {k}: {v}")
