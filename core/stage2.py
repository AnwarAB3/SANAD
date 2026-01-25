import streamlit as st
from core.report import generate_sanad_report, now_date_str
from core.review import (
    climate_voltage_check,
    compare_bom_vs_sld,
    extract_bom_signals,
    saudi_standards_snapshot,
    try_extract_from_sld,
)


# ==========================
# Styling (CSS only)
# ==========================
def _inject_css():
    st.markdown(
        """
<style>
/* Title + divider spacing */
.stage2-title{
  font-weight: 950;
  font-size: 1.18rem;
  margin: 0.2rem 0 0.7rem 0;
  letter-spacing: -0.01em;
}

/* Card */
.sg-card2{
  border-radius: 18px;
  padding: 14px 14px;
  margin: 0 0 14px 0;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(18, 28, 26, 0.62);
  box-shadow: 0 14px 34px rgba(0,0,0,0.35);
}
.sg-card2.ok{ border-color: rgba(46,196,182,0.55); background: rgba(46,196,182,0.075); }
.sg-card2.warn{ border-color: rgba(255,183,3,0.55); background: rgba(255,183,3,0.075); }
.sg-card2.crit{ border-color: rgba(230,57,70,0.55); background: rgba(230,57,70,0.075); }

/* Badge (one only) */
.badge{
  display:inline-flex;
  align-items:center;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 950;
  font-size: .78rem;
  letter-spacing: .08em;
  border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
  color: rgba(233,255,250,0.92);
}
.badge.ok{ border-color: rgba(46,196,182,0.55); }
.badge.warn{ border-color: rgba(255,183,3,0.55); }
.badge.crit{ border-color: rgba(230,57,70,0.55); }

/* Subtitle */
.sub{
  font-size: .90rem;
  color: rgba(233,255,250,0.72);
  margin-top: 2px;
  line-height: 1.35;
}

/* Bullets */
.bullets{
  margin-top: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
}
.bullets .item{
  margin: 6px 0;
  font-size: .93rem;
  color: rgba(233,255,250,0.88);
  line-height: 1.35;
}

/* KPI */
.kpi-box{
  border-radius: 16px;
  padding: 12px 12px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
}
.kpi-k{
  font-size:.76rem;
  color: rgba(233,255,250,0.60);
  text-transform: uppercase;
  letter-spacing:.06em;
}
.kpi-v{
  margin-top:4px;
  font-size:1.15rem;
  font-weight:950;
  color: rgba(233,255,250,0.96);
}

/* Section spacing */
.section-gap{ height: 8px; }
</style>
        """,
        unsafe_allow_html=True,
    )


def _level_class(level: str) -> str:
    level = (level or "WARN").upper()
    if level == "PASS":
        return "ok"
    if level == "WARN":
        return "warn"
    if level == "FAIL":
        return "crit"
    return "warn"


def _badge_text(level: str) -> str:
    level = (level or "WARN").upper()
    if level == "PASS":
        return "MATCH"
    if level == "WARN":
        return "WARNING"
    if level == "FAIL":
        return "CRITICAL"
    return ""


def _clean_lines(lines):
    out = []
    for x in lines or []:
        s = str(x).strip()
        if not s:
            continue
        # prevent stray html-ish tokens
        if s.lower() in ("</div>", "<div>", "</span>", "<span>"):
            continue
        if s.startswith("<") and s.endswith(">"):
            continue
        out.append(s)
    return out


def render_card(title, subtitle, level, bullets):
    cls = _level_class(level)
    badge = _badge_text(level)

    st.markdown(f'<div class="sg-card2 {cls}">', unsafe_allow_html=True)

    topL, topR = st.columns([1.35, 0.65])
    with topL:
        st.markdown(f"**{title}**")
        st.markdown(f'<div class="sub">{subtitle}</div>', unsafe_allow_html=True)

    with topR:
        if badge:
            st.markdown(
                f'<div class="badge {cls}">{badge}</div>', unsafe_allow_html=True
            )

    bullets = _clean_lines(bullets) or ["—"]

    st.markdown('<div class="bullets">', unsafe_allow_html=True)
    for b in bullets:
        st.markdown(f'<div class="item">• {b}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_kpis(items):
    cols = st.columns(len(items))
    for c, (k, v) in zip(cols, items):
        with c:
            st.markdown(
                f"""
                <div class="kpi-box">
                  <div class="kpi-k">{k}</div>
                  <div class="kpi-v">{v}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==========================
# Stage 2 main
# ==========================
def render_stage2():
    _inject_css()

    st.markdown(
        '<div class="stage2-title">Engineering review</div>', unsafe_allow_html=True
    )
    st.markdown('<div class="sg-divider"></div>', unsafe_allow_html=True)

    bom_df = st.session_state.get("bom_df")
    sld_bytes = st.session_state.get("sld_pdf_bytes")
    tmin = st.session_state.get("tmin")

    if bom_df is None or sld_bytes is None or tmin is None:
        st.error("Missing inputs. Complete Stage 1 first.")
        return

    # signals
    bom_sig = extract_bom_signals(bom_df)
    sld_sig = try_extract_from_sld(sld_bytes)

    # 1) BoM vs SLD
    doc = compare_bom_vs_sld(bom_sig, sld_sig)

    # per your requirement: INFO -> treat as PASS
    doc_level = (doc.level or "PASS").upper()
    if doc_level == "INFO":
        doc_level = "PASS"

    render_card(
        title="BoM vs SLD consistency",
        subtitle="Verifies whether the SLD drawing aligns with BoM key electrical values.",
        level=doc_level,
        bullets=doc.details,
    )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

    # 2) Climate check
    climate, numbers, recs = climate_voltage_check(bom_sig, float(tmin))

    render_kpis(
        [
            ("Inverter DC max", f"{numbers['Inverter_DC_max_V']:.0f} V"),
            ("Modules / string", f"{numbers['Modules_per_string']}"),
            ("Lowest temp (10y)", f"{numbers['Tmin_C']:.0f} °C"),
            ("String Voc @ Tmin", f"{numbers['String_Voc_at_Tmin_V']:.0f} V"),
        ]
    )

    render_card(
        title="Cold weather overvoltage risk",
        subtitle="Checks PV string voltage at minimum historical temperature.",
        level=climate.level,
        bullets=(climate.details + (recs or [])),
    )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

    # 3) Standards snapshot
    compliant, gaps = saudi_standards_snapshot(
        climate_ok=(climate.level == "PASS"),
        bom_sld_level=doc_level,
    )

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        render_card(
            title="Saudi / IEC snapshot — covered",
            subtitle="Checks satisfied in current submission.",
            level="PASS",
            bullets=compliant,
        )
    with c2:
        render_card(
            title="Saudi / IEC snapshot — gaps",
            subtitle="Items requiring attention before approval.",
            level=("WARN" if gaps else "PASS"),
            bullets=(gaps or ["No outstanding gaps detected."]),
        )

    # 4) Export
    st.markdown('<div class="sg-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="stage2-title">Export report</div>', unsafe_allow_html=True)

    payload = {
        "project_name": "SANAD",
        "place": st.session_state.get("place", "-"),
        "date_str": now_date_str(),
        "numbers": numbers,
        "bom_status": doc_level,
        "climate_status": climate.level,
        "compliant": compliant,
        "gaps": gaps,
        "recommendations": (recs or []),
    }

    pdf = generate_sanad_report(payload)

    st.download_button(
        "Download SANAD report (PDF)",
        data=pdf,
        file_name="SANAD_Design_Review_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
