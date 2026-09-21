"""Session 31 — fix fanzine reviews with distinct issue_number values."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Fanzine, FanzineReview

band = Band.objects.get(id=47)
rumore = Fanzine.objects.filter(name__icontains="Rumore").first()

# fix the first review's issue number
fr1 = FanzineReview.objects.filter(band=band, fanzine=rumore).first()
if fr1:
    fr1.issue_number = "online 19/01/2019"
    fr1.save()
    print("updated fr1:", fr1.id, fr1.issue_number)

# create second with distinct issue number
fr2, created = FanzineReview.objects.get_or_create(
    band=band, fanzine=rumore, issue_number="online 31/10/2019",
    defaults=dict(
        year=2019,
        review_text="Prima ristampa mai realizzata di 'Stanze' (1993): remaster dai nastri, formato digitale, vinile e CD, nuovo tour.",
        digitized_url="https://rumoremag.com/2019/10/31/massimo-volume-tour-ristampa-stanze/",
        notes="Online article on rumoremag.com (Rumore magazine official site).",
    ),
)
print("fr2:", fr2.id, "created:", created)

print("MV fanzine reviews:", FanzineReview.objects.filter(band=band).count())
print("FINAL LINK COUNT:", band.links.count())
