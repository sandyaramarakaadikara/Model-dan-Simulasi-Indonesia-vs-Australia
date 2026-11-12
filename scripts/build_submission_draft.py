"""Build the blinded journal manuscript and separate title page from Markdown.

Uses the bundled python-docx runtime. The source Markdown remains the editable
content master; Word files follow the target journal's published checklist.
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
MANUSCRIPT_DIR = PROJECT_ROOT / "docs" / "manuscript"
FIGURES_DIR = PROJECT_ROOT / "figures"

def resolve_doc_file(filename: str) -> Path:
    for cand in [MANUSCRIPT_DIR / filename, PROJECT_ROOT / filename, ROOT / filename]:
        if cand.exists():
            return cand
    return MANUSCRIPT_DIR / filename

SOURCE = resolve_doc_file("Naskah_Revisi_Exploratory_Indonesia_Australia_EN.md")
MANUSCRIPT = MANUSCRIPT_DIR / "Manuscript_Blind_Review_Jurnal_Pertahanan_EN.docx"
TITLE_PAGE = MANUSCRIPT_DIR / "Title_Page_Jurnal_Pertahanan_EN.docx"
FIGURE = FIGURES_DIR / "perubahan_belanja_dan_impor_WDI_12negara_lengkap.png"

def set_cell_shading(cell, fill="EAF0F6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)

def style_run(run, size=12, bold=False, italic=False):
    run.font.name = "Cambria"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Cambria")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic

def add_rich_text(paragraph, text, size=12):
    # Minimal Markdown emphasis support; all other text remains literal.
    pieces = re.split(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)", text)
    for piece in pieces:
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            run = paragraph.add_run(piece[2:-2]); style_run(run, size=size, bold=True)
        elif piece.startswith("*") and piece.endswith("*"):
            run = paragraph.add_run(piece[1:-1]); style_run(run, size=size, italic=True)
        elif piece.startswith("`") and piece.endswith("`"):
            run = paragraph.add_run(piece[1:-1]); style_run(run, size=size)
        else:
            run = paragraph.add_run(piece); style_run(run, size=size)

def setup_document(doc, anonymous=True):
    sec = doc.sections[0]
    sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.54); sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54); sec.right_margin = Cm(2.54)
    normal = doc.styles["Normal"]
    normal.font.name = "Cambria"; normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Cambria")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for nm, size in [("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 12)]:
        st = doc.styles[nm]
        st.font.name = "Cambria"; st._element.rPr.rFonts.set(qn("w:eastAsia"), "Cambria")
        st.font.size = Pt(size); st.font.bold = True
        st.paragraph_format.space_before = Pt(10); st.paragraph_format.space_after = Pt(3)
        st.paragraph_format.keep_with_next = True
    props = doc.core_properties
    props.author = "" if anonymous else "Sandyarama Raka Adikara; Fauzan Akbar Ansyori; Nazmi Priyatama Suherman"
    props.last_modified_by = "" if anonymous else "Sandyarama Raka Adikara"
    props.title = "Military Expenditure and the WDI Arms-Import Indicator in Selected Indo-Pacific Economies, 2010–2025"
    props.subject = "Exploratory descriptive comparison"

def add_markdown_table(doc, rows):
    cleaned = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
    if len(cleaned) > 1 and all(re.fullmatch(r"\s*:?-{3,}:?\s*", c) for c in cleaned[1]):
        cleaned.pop(1)
    table = doc.add_table(rows=1, cols=len(cleaned[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    set_repeat_table_header(table.rows[0])
    for j, val in enumerate(cleaned[0]):
        cell = table.rows[0].cells[j]; cell.text = ""
        set_cell_shading(cell)
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_rich_text(p, val, size=9)
        for r in p.runs: r.bold = True
    for values in cleaned[1:]:
        cells = table.add_row().cells
        for j, val in enumerate(values):
            cells[j].text = ""
            cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[j].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 or "Not calculated" in val else WD_ALIGN_PARAGRAPH.CENTER
            add_rich_text(p, val, size=9)
    doc.add_paragraph()

def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)

def build_manuscript():
    doc = Document(); setup_document(doc, anonymous=True)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 0; keywords_mode = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if keywords_mode and not line.startswith("#"):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_rich_text(p, line, size=11)
            i += 1; continue
        if line.startswith("# "):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(8)
            add_rich_text(p, line[2:].upper(), size=14)
            for run in p.runs: run.bold = True
            i += 1; continue
        if line.startswith("## "):
            keywords_mode = False
            title = line[3:]
            if title in {"Abstract", "Keywords"}:
                p = doc.add_paragraph(style="Heading 2"); p.add_run(title)
            elif title == "References":
                doc.add_page_break(); p = doc.add_paragraph(style="Heading 1"); p.add_run("References")
            else:
                p = doc.add_paragraph(style="Heading 1"); p.add_run(title)
            i += 1; continue
        if line.startswith("### "):
            p = doc.add_paragraph(style="Heading 2"); p.add_run(line[4:])
            i += 1; continue
        if line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            add_markdown_table(doc, rows); continue
        image_match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
        if image_match:
            raw_img_path = image_match.group(2).strip()
            img_name = Path(raw_img_path).name
            resolved_img = None
            for cand in [
                FIGURES_DIR / img_name,
                PROJECT_ROOT / raw_img_path,
                SOURCE.parent / raw_img_path,
                ROOT / raw_img_path,
            ]:
                if cand.exists():
                    resolved_img = cand
                    break
            if resolved_img:
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run().add_picture(str(resolved_img), width=Inches(6.2))
            i += 1; continue
        if line.startswith("**Figure ") or line.startswith("**Table "):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_rich_text(p, line, size=10); i += 1; continue
        if line.startswith("> "):
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.5)
            add_rich_text(p, line[2:], size=11); i += 1; continue
        p = doc.add_paragraph()
        if line.startswith("**Keywords:**"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_rich_text(p, "**Keywords:**", size=11)
            keywords_mode = True
        elif line.startswith("**Note.**"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_rich_text(p, line, size=9)
        elif line.startswith("Christie,") or line.startswith("George,") or line.startswith("Himawan,") or line.startswith("Rasyid,") or line.startswith("Stockholm International Peace Research Institute.") or line.startswith("Tian,") or line.startswith("World Bank."):
            p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_rich_text(p, line, size=10)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_rich_text(p, line, size=12)
        i += 1
    for section in doc.sections:
        add_page_number(section.footer.paragraphs[0])
    doc.save(MANUSCRIPT)

def build_title_page():
    doc = Document(); setup_document(doc, anonymous=False)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_rich_text(p, "STOCHASTIC MONTE CARLO SIMULATION AND MULTI-CRITERIA CAPABILITY COMPARISON OF INDONESIAN AND AUSTRALIAN DEFENSE RESOURCE ALLOCATIONS (2010–2025)", size=14)
    for r in p.runs: r.bold = True
    p.paragraph_format.space_after = Pt(20)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_rich_text(p, "Sandyarama Raka Adikara¹*, Fauzan Akbar Ansyori¹, Nazmi Priyatama Shuerman¹", size=11)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_rich_text(p, "¹Program Studi Teknik Informatika, Fakultas Ilmu Komputer dan Sistem Informasi, Universitas Kebangsaan Republik Indonesia, Bandung, Indonesia", size=11)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_rich_text(p, "*Corresponding author: sandyarama.raka@student.ukri.ac.id", size=11)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_rich_text(p, "Article type: Research Paper — Modeling and Simulation", size=11)
    doc.save(TITLE_PAGE)

if __name__ == "__main__":
    build_manuscript(); build_title_page()
    print(MANUSCRIPT.name); print(TITLE_PAGE.name)
