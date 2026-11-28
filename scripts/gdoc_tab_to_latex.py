"""Convert one tab of the thesis Google Doc (saved `read_doc` JSON) to a LaTeX chapter body (conventions: docs/PANDUAN-GDOCS.md).

    python -I scripts/gdoc_tab_to_latex.py <read_doc.json> <tabId> <out.tex> [--label pendahuluan]

- HEADING_1 -> \\chapter{<second line>} ; HEADING_2 -> \\section ; HEADING_3 -> \\subsection (typed numbers "I.2." removed)
- NORMAL_TEXT -> paragraph; italic runs -> \\textit{}; bold runs -> \\textbf{}
- [@a; @b] -> \\cite{a,b}
- bulleted paragraphs -> enumerate (DECIMAL glyph) or itemize
- the grey italic "Draf berbantuan AI ..." note paragraph is skipped
"""
import json
import re
import sys

LATEX_ESC = {"\\": r"\textbackslash{}", "%": r"\%", "&": r"\&", "#": r"\#", "_": r"\_", "$": r"\$", "{": r"\{", "}": r"\}",
             "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def esc(s: str) -> str:
    return "".join(LATEX_ESC.get(c, c) for c in s)


def label_of(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def run_text(run) -> str:
    tr = run.get("textRun")
    if not tr:
        return ""
    raw = tr["content"].replace("\n", "").replace("\x0b", " ")
    st = tr.get("textStyle", {})
    # protect citations before escaping
    parts = re.split(r"(\[@[^\]]+\])", raw)
    out = []
    for p in parts:
        if p.startswith("[@"):
            keys = [k.strip().lstrip("@") for k in p[1:-1].split(";")]
            out.append(r"\cite{" + ",".join(keys) + "}")
        else:
            out.append(esc(p))
    s = "".join(out)
    if not s.strip():
        return s
    if st.get("italic"):
        s = r"\textit{" + s + "}"
    if st.get("bold"):
        s = r"\textbf{" + s + "}"
    return s


def main():
    src, tab_id, out = sys.argv[1], sys.argv[2], sys.argv[3]
    d = json.load(open(src, encoding="utf-8"))
    d = d.get("content", d)

    def walk(tabs):
        for t in tabs:
            yield t
            yield from walk(t.get("childTabs", []))

    tab = next(t for t in walk(d["tabs"]) if t["tabProperties"]["tabId"] == tab_id)
    lists = tab["documentTab"].get("lists", {})
    lines, open_list = [], None
    for el in tab["documentTab"]["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        style = p["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT")
        plain = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"]).strip()
        if not plain:
            continue
        if plain.startswith("Draf berbantuan AI"):
            continue
        bullet = p.get("bullet")
        kind = None
        if bullet:
            lvl0 = lists.get(bullet["listId"], {}).get("listProperties", {}).get("nestingLevels", [{}])[0]
            kind = "enumerate" if lvl0.get("glyphType", "").startswith(("DECIMAL", "ALPHA", "ROMAN", "UPPER")) else "itemize"
        if open_list and kind != open_list:
            lines.append(rf"\end{{{open_list}}}" + "\n")
            open_list = None
        if style == "HEADING_1":
            title = plain.split("\x0b")[-1].strip() if "\x0b" in plain else plain
            lines.append(rf"\chapter{{{title}}}\label{{{label_of(title)}}}" + "\n")
            continue
        if style in ("HEADING_2", "HEADING_3"):
            title = re.sub(r"^[IVX]+(\.\d+)+\.?\s*", "", plain)
            cmd = "section" if style == "HEADING_2" else "subsection"
            lines.append(rf"\{cmd}{{{esc(title)}}}\label{{{label_of(title)}}}" + "\n")
            continue
        body = "".join(run_text(e) for e in p["elements"]).strip()
        if kind:
            if not open_list:
                lines.append(rf"\begin{{{kind}}}")
                open_list = kind
            lines.append(r"  \item " + body)
        else:
            lines.append(body + "\n")
    if open_list:
        lines.append(rf"\end{{{open_list}}}" + "\n")
    header = (f"% Dikonversi otomatis dari Google Docs (tab {tab_id}) dengan scripts/gdoc_tab_to_latex.py.\n"
              "% Sejak konversi, revisi bab ini dilakukan di file .tex ini (docs/PANDUAN-GDOCS.md).\n")
    open(out, "w", encoding="utf-8").write(header + "\n".join(lines))
    print(f"{out}: {len(lines)} blok")


if __name__ == "__main__":
    main()
