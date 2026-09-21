"""Session 31 — inspect IA metadata files for relevance."""
import json

for name, ident in [
    ("s31_iameta_massimo-volume-vittoria", "massimo-volume-vittoria-burattini"),
    ("s31_iameta_42IlNuotatoreCheever", "42IlNuotatoreCheever"),
    ("s31_iameta_la_citta_futura-5-6_20", "la_citta_futura-5-6_2000"),
    ("s31_iameta_Roxyto2406_04_2011", "Roxyto2406.04.2011"),
]:
    try:
        d = json.load(open("/tmp/%s.txt" % name, encoding="utf-8", errors="ignore"))
    except Exception as e:
        print(ident, "PARSE_ERR", e)
        continue
    md = d.get("metadata", {})
    print("=" * 15, ident, "=" * 15)
    for k in ["identifier", "title", "description", "creator", "date", "mediatype"]:
        v = md.get(k)
        if v:
            v = str(v)[:300].replace("\n", " ")
            print(f"{k}: {v}")
    files = d.get("files", [])
    audio = [f.get("name") for f in files if f.get("format") in ("VBR MP3", "Ogg Vorbis", "Flac") or (f.get("name") or "").endswith((".mp3", ".ogg", ".flac"))]
    for a in audio[:8]:
        print("  AUDIO:", a)
    print("  total files:", len(files))
    print()
