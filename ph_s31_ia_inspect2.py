"""Session 31 — inspect remaining IA metadata (fixed filenames)."""
import json

for name in ["/tmp/s31_iameta_massimo-volume-vittoria-.txt",
             "/tmp/s31_iameta_la_citta_futura-5-6_20.txt"]:
    d = json.load(open(name, encoding="utf-8", errors="ignore"))
    md = d.get("metadata", {})
    print("=" * 15, md.get("identifier"), "=" * 15)
    for k in ["identifier", "title", "description", "creator", "date", "mediatype"]:
        v = md.get(k)
        if v:
            v = str(v)[:400].replace("\n", " ")
            print(f"{k}: {v}")
    files = d.get("files", [])
    audio = [f.get("name") for f in files if (f.get("name") or "").endswith((".mp3", ".ogg", ".flac"))]
    for a in audio[:8]:
        print("  AUDIO:", a)
    print("  total files:", len(files))
    print()
