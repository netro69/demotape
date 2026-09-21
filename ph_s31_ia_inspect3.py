"""Session 31 — full descriptions of IA items matching 'massimo volume'."""
import json

for name in ["/tmp/s31_iameta_la_citta_futura-5-6_2000.txt",
             "/tmp/s31_iameta_42IlNuotatoreCheever.txt",
             "/tmp/s31_iameta_Roxyto2406_04_2011.txt"]:
    d = json.load(open(name, encoding="utf-8", errors="ignore"))
    md = d.get("metadata", {})
    print("=" * 15, md.get("identifier"), "=" * 15)
    desc = str(md.get("description", ""))
    # find mentions of massimo volume
    idx = desc.lower().find("massimo")
    if idx >= 0:
        s = max(0, idx - 200)
        print("MV CTX:", desc[s:idx + 300].replace("\n", " "))
    else:
        print("DESC:", desc[:400].replace("\n", " "))
    files = d.get("files", [])
    for f in files[:6]:
        print("  FILE:", f.get("name"), "|", f.get("format"))
    print()
