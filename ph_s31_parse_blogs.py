"""Session 31 — parse blog posts for Demo Nero download links and tracklists."""
import html
import re

for name in ["radiomolotov", "breakfastjumpers"]:
    raw = open("/tmp/s31_%s.txt" % name, encoding="utf-8", errors="ignore").read()
    print("=" * 20, name, "=" * 20)
    urls = re.findall(r'href=["\x27](https?://[^"\x27]+)["\x27]', raw)
    keep = [u for u in urls if any(k in u.lower() for k in [
        "mediafire", "megaupload", "rapidshare", "mega.nz", "zippyshare",
        "sendspace", "4shared", "depositfiles", "download", ".rar", ".zip",
        ".mp3", "rapidgator", "turbo", "wetransfer"])]
    for u in sorted(set(keep))[:20]:
        print("LINK:", u)
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(re.sub(r"\s+", " ", txt))
    m = re.search(r"[Dd]emo", txt)
    if m:
        s = max(0, m.start() - 150)
        print("CTX:", txt[s:m.start() + 250].strip()[:400])
    m2 = re.search(r"tracklist|brani", txt, re.I)
    if m2:
        print("TRACKS:", txt[m2.start():m2.start() + 450])
    print()
