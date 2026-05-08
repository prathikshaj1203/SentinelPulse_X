"""System Logs — diagnostic + system event logs."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from utils.theme import apply_theme
from utils.logger import DIAG_LOG, SYS_LOG, read_log, log_system

st.set_page_config(page_title="System Logs · Sentinel Pulse", layout="wide")
apply_theme()
log_system("logs_view")

st.markdown("### System Logs")
st.markdown("<div class='sp-muted'>Audit trail of diagnostics and system events.</div>",
            unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Diagnostics", "System events"])

with tab1:
    df = read_log(DIAG_LOG)
    if df.empty:
        st.info("No diagnostics logged yet.")
    else:
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)

with tab2:
    df = read_log(SYS_LOG)
    if df.empty:
        st.info("No system events yet.")
    else:
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
