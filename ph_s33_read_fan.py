"""Session 33 — print full fan storia + dilemmi + down pages."""
BASE = "/home/ubuntu/Projects/demotape/research_output/"

for f in ["s33_fan_storia.txt", "s33_fan_dilemmi.txt", "s33_fan_down.txt"]:
    t = open(BASE + f, encoding="utf-8").read()
    print("=" * 25, f, "=" * 25)
    print(t)
    print()
