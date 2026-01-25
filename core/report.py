import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_sanad_report(payload: dict) -> bytes:
    """
    payload keys expected:
      project_name, place, date_str
      section_status: list of {title, level, details}
      numbers: dict
      compliant: list
      gaps: list
      recommendations: list
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    def txt(x, y, s, size=10, bold=False):
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, s)

    def wrap_lines(s: str, max_len: int = 95):
        words = s.split()
        lines, line = [], []
        for word in words:
            if len(" ".join(line + [word])) <= max_len:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        if line:
            lines.append(" ".join(line))
        return lines

    # Header
    y = h - 2.0 * cm
    txt(2.0 * cm, y, payload.get("project_name", "SANAD"), size=20, bold=True)
    y -= 0.55 * cm
    txt(2.0 * cm, y, "PV Design Review Report", size=12, bold=True)
    y -= 0.50 * cm
    txt(2.0 * cm, y, f"Site: {payload.get('place', '-')}", size=10)
    y -= 0.40 * cm
    txt(2.0 * cm, y, f"Date: {payload.get('date_str', '-')}", size=10)

    y -= 0.55 * cm
    c.line(2.0 * cm, y, w - 2.0 * cm, y)
    y -= 0.55 * cm

    # Summary status
    txt(2.0 * cm, y, "Summary", size=12, bold=True)
    y -= 0.45 * cm

    for sec in payload.get("section_status", []):
        title = sec.get("title", "")
        level = sec.get("level", "")
        details = sec.get("details", [])
        txt(2.0 * cm, y, f"{title} — {level}", size=10, bold=True)
        y -= 0.40 * cm
        for d in details[:3]:
            for line in wrap_lines(f"- {d}", 100):
                txt(2.2 * cm, y, line, size=9)
                y -= 0.35 * cm
        y -= 0.15 * cm

    # Key numbers
    txt(2.0 * cm, y, "Key Numbers", size=12, bold=True)
    y -= 0.45 * cm
    for k, v in payload.get("numbers", {}).items():
        txt(2.2 * cm, y, f"{k}: {v}", size=9)
        y -= 0.32 * cm
        if y < 3.2 * cm:
            c.showPage()
            y = h - 2.0 * cm

    y -= 0.20 * cm

    # Compliance
    txt(2.0 * cm, y, "Saudi/IEC Snapshot", size=12, bold=True)
    y -= 0.45 * cm
    txt(2.2 * cm, y, "Compliant / Covered:", size=10, bold=True)
    y -= 0.40 * cm
    for it in payload.get("compliant", [])[:6]:
        for line in wrap_lines(f"• {it}", 100):
            txt(2.35 * cm, y, line, size=9)
            y -= 0.32 * cm
    y -= 0.15 * cm

    txt(2.2 * cm, y, "Gaps / Actions required:", size=10, bold=True)
    y -= 0.40 * cm
    for it in payload.get("gaps", [])[:9]:
        for line in wrap_lines(f"• {it}", 100):
            txt(2.35 * cm, y, line, size=9)
            y -= 0.32 * cm
        if y < 3.2 * cm:
            c.showPage()
            y = h - 2.0 * cm

    y -= 0.20 * cm

    # Recommendations
    txt(2.0 * cm, y, "Recommendations", size=12, bold=True)
    y -= 0.45 * cm
    recs = payload.get("recommendations", [])
    if not recs:
        recs = ["No critical actions required based on the provided inputs."]
    for r in recs[:10]:
        for line in wrap_lines(f"• {r}", 100):
            txt(2.2 * cm, y, line, size=9)
            y -= 0.32 * cm
        if y < 3.2 * cm:
            c.showPage()
            y = h - 2.0 * cm

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()


def now_date_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")
