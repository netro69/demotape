# Session 40 target selection — most under-researched era-true Italian band
import re
from django.db.models import Count
from apps.core.models import Band, Link, Release, FanzineReview, Fanzine

COVERED = [
    'clark-nova', 'negrita', 'afterhours', 'cut', 'marlene-kuntz', 'prozac',
    'thee-stolen-cars', 'ustmamo', 'rock-rose', 'rockrose', 'blak-vomit',
    'cccp', 'peggio-punx', 'one-dimensional-man', 'gli-avvoltoi', 'declino',
    'plastik', 'asphodel', 'bartok', 'mao-e-la-rivoluzione', 'massimo-volume',
    'mind-drop', 'rockgalileo', 'timoria', 'scarlett', 'the-groovers',
    'pankow', 'julies-haircut',
]

def parse_years(s):
    if not s:
        return None, None
    s = s.strip()
    m = re.match(r'^(?:c\.?\s*)?(\d{4})\s*[-\u2013\u2014~]+\s*(\d{4}|present|oggi|attual[aei]?|attiv[oi]?)?\s*$', s, re.I)
    if m:
        start = int(m.group(1))
        end_raw = (m.group(2) or '').lower()
        if re.match(r'^\d{4}$', end_raw):
            return start, int(end_raw)
        return start, None
    m2 = re.match(r'^(?:c\.?\s*)?(\d{4})s\b', s)
    if m2:
        d = int(m2.group(1))
        return d, d + 9
    return None, None

print('=== CANDIDATES (published, not covered, sorted by link count) ===')
rows = []
for b in Band.objects.filter(status='published').annotate(nl=Count('links')):
    if b.slug in COVERED:
        continue
    s, e = parse_years(b.active_years)
    if s is None:
        era = '?'
    else:
        e2 = e if e is not None else 2026
        era = 'YES' if (s <= 2000 and e2 >= 1985) else 'no'
    nrel = b.releases.count()
    rows.append((b.nl, b.name, b.slug, str(b.city), str(b.active_years), s, e, era, b.id, nrel))

rows.sort(key=lambda r: (r[0], r[1].lower()))
for r in rows[:45]:
    print(f'id={r[8]:4d} | {r[0]:3d} lnk | {r[9]:2d} rel | {r[1][:30]:30s} | {r[3][:20]:20s} | {r[4][:22]:22s} | {r[5]}-{r[6]} | era={r[7]}')

print()
print('Total published bands:', Band.objects.filter(status='published').count())
print('Total links:', Link.objects.count())
print('Total releases:', Release.objects.count())
print('Total fanzines:', Fanzine.objects.count())
print('Total fanzine reviews:', FanzineReview.objects.count())
