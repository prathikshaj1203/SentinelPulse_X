"""System Logs — diagnostic + system event logs."""

import sys
from pathlib import Path
from utils.sidebar import render_sidebar
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from utils.theme import apply_theme
from database.db import fetch_predictions

st.set_page_config(
    page_title="System Logs · Sentinel Pulse",
    layout="wide"
)

apply_theme()
render_sidebar()

st.markdown("### System Logs")

st.markdown(
    "<div class='sp-muted'>Audit trail of diagnostics and system events.</div>",
    unsafe_allow_html=True
)

# ---------------- POSTGRESQL LOGS ---------------- #

st.markdown("## 📡 PostgreSQL Diagnostic Records")

df = fetch_predictions()

if not df.empty:

    st.dataframe(
        df.iloc[::-1],
        width='stretch',
        hide_index=True
    )

else:

    st.info("No PostgreSQL records found.")