"""Generate pcf_paper_draft.tex from template + table15.json (draft 2026-10-06)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "table15.json")))
tab = "\n".join(f"C{r[0]} & ${r[1]}$ & ${r[2]}$ & ${r[3][:22]}\\ldots$ & ${r[5]}$ \\\\" for r in rows)
tpl = open(os.path.join(HERE, "pcf_paper_template.tex"), encoding="utf-8").read()
open(os.path.join(HERE, "pcf_paper_draft.tex"), "w", encoding="utf-8").write(tpl.replace("%%TABLE%%", tab))
print("ok")
