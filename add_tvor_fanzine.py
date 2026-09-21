#!/usr/bin/env python
"""Add T.V.O.R. Teste Vuote Ossa Rotte as a Fanzine (verified existence)."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Fanzine

# Check if TVOR already exists
slug = 'tvor-teste-vuote-ossa-rotte'
existing = Fanzine.objects.filter(slug=slug).first()
if existing:
    print(f"Fanzine already exists: {existing.name} (slug={existing.slug})")
    print(f"  ID={existing.id}")
    print(f"  Status: {existing.status}")
    print(f"  Website: {existing.website}")
else:
    print("Creating T.V.O.R. Teste Vuote Ossa Rotte fanzine...")
    try:
        fanzine = Fanzine.objects.create(
            name='T.V.O.R. Teste Vuote Ossa Rotte',
            slug=slug,
            city='Como',
            active_years='1981-1985',
            description='Italian hardcore punk fanzine (chaoszine) founded by Stiv Rottame and Marco Maniglia. Published 5 issues 1981-1985. Print run: 500 copies per issue. One of the most influential punk fanzines in Italy and internationally (reviewed in Maximum Rock\'n\'Roll #42). Primary documentation source for the early Italian hardcore punk scene (Negazione, Declino, Blue Vomit, Nerorgasmo, etc.).',
            status='defunct',
            website='https://it.wikipedia.org/wiki/T.V.O.R._Teste_Vuote_Ossa_Rotte',
        )
        print(f"Created Fanzine: {fanzine.name} (ID={fanzine.id})")
        print(f"  Slug: {fanzine.slug}")
        print(f"  Status: {fanzine.status}")
    except Exception as e:
        print(f"Error: {e}")

# List all fanzines
print("\n=== ALL FANZINES ===")
for f in Fanzine.objects.all():
    print(f"  [{f.status}] {f.name} ({f.city}, {f.active_years})")
