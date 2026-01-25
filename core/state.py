import streamlit as st


def init_state():
    st.session_state.setdefault("stage", 1)

    st.session_state.setdefault("geo_results", None)
    st.session_state.setdefault("place", None)
    st.session_state.setdefault("lat", None)
    st.session_state.setdefault("lon", None)

    st.session_state.setdefault("current_temp", None)
    st.session_state.setdefault("tmin", None)
    st.session_state.setdefault("tmin_method", None)

    st.session_state.setdefault("sld_pdf_name", None)
    st.session_state.setdefault("sld_pdf_bytes", None)

    st.session_state.setdefault("bom_df", None)
    st.session_state.setdefault("bom_name", None)


def reset_all():
    for k in [
        "stage",
        "geo_results",
        "place",
        "lat",
        "lon",
        "current_temp",
        "tmin",
        "tmin_method",
        "sld_pdf_name",
        "sld_pdf_bytes",
        "bom_df",
        "bom_name",
    ]:
        if k in st.session_state:
            del st.session_state[k]
    init_state()
