import streamlit as st


def apply_theme():
    st.markdown(
        """
<style>


:root{
  --bg-main:#0B1F1B;
  --bg-grad1:#153B33;
  --bg-grad2:#1E4F44;

  --brand:#5FAF9E;
  --brand-soft:#7CCFC1;
  --accent:#9FE3D6;

  --text-main:#FFFFFF;
  --text-muted:rgba(255,255,255,0.75);

  --border:rgba(159,227,214,0.25);
}

/* Background */
html, body, [data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1200px 600px at 20% 0%, rgba(95,175,158,0.25), transparent 60%),
    radial-gradient(900px 520px at 85% 25%, rgba(124,207,193,0.18), transparent 55%),
    linear-gradient(180deg, var(--bg-grad2), var(--bg-main));
  color: var(--text-main);
}

/* Layout */
.block-container{
  max-width: 1320px;
  padding-top: 2.2rem;
  padding-bottom: 2.2rem;
}

/* Header */
.sg-header{ margin-bottom: 18px; }

.sg-title{
  font-size: 3.2rem;
  font-weight: 1000;
  letter-spacing: 0.08em;
  line-height: 1.05;
  text-transform: uppercase;
  color: var(--text-main);
}

.sg-subtitle{
  margin-top: 12px;
  font-size: 1.05rem;
  color: var(--text-muted);
  border-left: 4px solid var(--brand);
  padding-left: 14px;
  max-width: 780px;
}

/* Divider */
.sg-divider{
  height: 1px;
  background: var(--border);
  margin: 18px 0 22px 0;
}

/* Section titles */
.sg-h2{
  font-size: 1.05rem;
  font-weight: 900;
  letter-spacing: -0.01em;
  color: var(--text-main);
  margin-bottom: 10px;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div{
  border-radius: 12px !important;
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--border) !important;
  color: white !important;
}

/* Upload */
[data-testid="stFileUploader"] section{
  background: rgba(255,255,255,0.03);
  border: 1px dashed var(--border);
  border-radius: 12px;
}

/* Buttons */
.sg-btn-primary button{
  background: linear-gradient(135deg, #5FAF9E, #7CCFC1) !important;
  border: 0 !important;
  border-radius: 14px !important;
  color: #06362E !important;
  font-weight: 950 !important;
  padding: 0.78rem 1.15rem !important;
  transition: all 0.25s ease;
}

.sg-btn-primary button:hover{
  background: linear-gradient(135deg, #7CCFC1, #9FE3D6) !important;
  transform: translateY(-1px);
}

.sg-btn-ghost button{
  background: rgba(95,175,158,0.18) !important;
  border: 1px solid rgba(159,227,214,0.45) !important;
  border-radius: 14px !important;
  color: #E9FFFA !important;
  font-weight: 900 !important;
  padding: 0.75rem 1.1rem !important;
}

.sg-btn-clean button{
  background: rgba(95,175,158,0.14) !important;
  border: 1px solid rgba(159,227,214,0.35) !important;
  border-radius: 14px !important;
  color: #E9FFFA !important;
  font-weight: 900 !important;
  padding: 0.75rem 1.1rem !important;
}

/* Weather block */
.sg-weather{
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.04);
  border-radius: 16px;
  padding: 16px;
}

.sg-label{
  font-size: 0.85rem;
  font-weight: 850;
  color: var(--text-muted);
}

.sg-temp{
  font-size: 2.2rem;
  font-weight: 1000;
  letter-spacing: -0.02em;
}

.sg-unit{
  font-size: 1.05rem;
  margin-left: 6px;
  opacity: 0.85;
}

.sg-chip{
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.04);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 0.82rem;
  font-weight: 850;
  color: var(--text-muted);
}

/* iframe cleanup */
iframe{
  background: transparent !important;
  border: 0 !important;
}


div.stButton > button,
[data-testid="stFileUploader"] button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"]{
  background: rgba(95,175,158,0.16) !important;
  border: 1px solid rgba(159,227,214,0.45) !important;
  color: #E9FFFA !important;
  border-radius: 14px !important;
  font-weight: 900 !important;
}

div.stButton > button[kind="primary"],
[data-testid="baseButton-primary"]{
  background: linear-gradient(135deg,#5FAF9E,#7CCFC1) !important;
  border: 0 !important;
  color: #06362E !important;
  font-weight: 950 !important;
}

/* Hover */
div.stButton > button:hover,
[data-testid="stFileUploader"] button:hover{
  background: linear-gradient(135deg,#7CCFC1,#9FE3D6) !important;
  transform: translateY(-1px);
}

/* File uploader container */
[data-testid="stFileUploader"] section{
  background: rgba(255,255,255,0.03) !important;
  border: 1px dashed rgba(159,227,214,0.35) !important;
  border-radius: 14px !important;
}



.stTextInput input,
[data-testid="stTextInput"] input,
input[type="text"]{
  background: rgba(95,175,158,0.12) !important;
  border: 1px solid rgba(159,227,214,0.55) !important;
  color: #E9FFFA !important;
  border-radius: 14px !important;
  font-weight: 850 !important;
}

div[data-baseweb="input"] input{
  background: rgba(95,175,158,0.12) !important;
  border: 1px solid rgba(159,227,214,0.55) !important;
  color: #E9FFFA !important;
  border-radius: 14px !important;
  font-weight: 850 !important;
}

/* placeholder */
.stTextInput input::placeholder,
[data-testid="stTextInput"] input::placeholder,
div[data-baseweb="input"] input::placeholder{
  color: rgba(233,255,250,0.55) !important;
}

/* focus */
.stTextInput input:focus,
[data-testid="stTextInput"] input:focus,
div[data-baseweb="input"] input:focus{
  border: 1px solid rgba(124,207,193,0.95) !important;
  box-shadow: 0 0 0 4px rgba(95,175,158,0.22) !important;
  outline: none !important;
}

div[data-baseweb="input"]{
  background: transparent !important;
}

[data-testid="stTextInput"]{
  background: transparent !important;
}


.sg-res{
  border: 1px solid rgba(159,227,214,0.22);
  background: rgba(10, 18, 23, 0.62);
  border-radius: 18px;
  padding: 14px 14px;
  margin: 0 0 14px 0;
  box-shadow: 0 14px 34px rgba(0,0,0,0.35);
}

.sg-res-top{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:14px;
}

.sg-res-title{
  font-size: 1.05rem;
  font-weight: 900;
  letter-spacing: -0.01em;
  color: rgba(233,255,250,0.96);
}

.sg-res-sub{
  margin-top: 4px;
  font-size: 0.90rem;
  color: rgba(233,255,250,0.70);
  line-height: 1.35;
}

.sg-res-right{ text-align:right; display:flex; flex-direction:column; gap:10px; align-items:flex-end; }

.sg-res-badge{
  padding: 7px 12px;
  border-radius: 999px;
  font-weight: 900;
  font-size: 0.82rem;
  letter-spacing: .08em;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  color: rgba(233,255,250,0.92);
}

.sg-res-metric{
  border-radius: 14px;
  padding: 8px 10px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.05);
  min-width: 165px;
}
.sg-res-metric .k{
  font-size: 0.78rem;
  color: rgba(233,255,250,0.60);
  text-transform: uppercase;
  letter-spacing: .06em;
}
.sg-res-metric .v{
  margin-top: 2px;
  font-size: 1.02rem;
  font-weight: 950;
  color: rgba(233,255,250,0.96);
}

.sg-res-body{ margin-top: 12px; }
.sg-res-body ul{ margin:0; padding-left: 18px; }
.sg-res-body li{
  margin: 6px 0;
  color: rgba(233,255,250,0.82);
  font-size: 0.92rem;
  line-height: 1.35;
}

/* color accents */
.sg-res.pass{ border-color: rgba(46,196,182,0.42); background: rgba(46,196,182,0.08); }
.sg-res.warn{ border-color: rgba(255,183,3,0.40); background: rgba(255,183,3,0.08); }
.sg-res.fail{ border-color: rgba(230,57,70,0.40); background: rgba(230,57,70,0.08); }
.sg-res.info{ border-color: rgba(58,134,255,0.36); background: rgba(58,134,255,0.06); }

/* KPI grid */
.sg-kpi-grid{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 12px 0 6px 0;
}
@media (max-width: 1100px){
  .sg-kpi-grid{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
.sg-kpi{
  border-radius: 16px;
  padding: 12px 12px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.05);
}
.sg-kpi .l{
  font-size: 0.78rem;
  color: rgba(233,255,250,0.60);
  text-transform: uppercase;
  letter-spacing: .06em;
}
.sg-kpi .v{
  margin-top: 4px;
  font-size: 1.15rem;
  font-weight: 950;
  color: rgba(233,255,250,0.96);
}

</style>
""",
        unsafe_allow_html=True,
    )
