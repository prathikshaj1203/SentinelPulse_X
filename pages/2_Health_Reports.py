"""Health Reports — analytics over diagnostic history."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.theme import apply_theme
from utils.logger import DIAG_LOG, read_log, log_system

st.set_page_config(page_title="Health Reports · Sentinel Pulse", layout="wide")
apply_theme()
log_system("reports_view")

st.markdown("### Health Reports")
st.markdown("<div class='sp-muted'>Diagnostic history, severity distribution, and maintenance trends.</div>",
            unsafe_allow_html=True)
st.write("")

df = read_log(DIAG_LOG)
if df.empty:
    st.info("No diagnostic data yet. Run a few diagnoses first.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

c1, c2, c3 = st.columns(3)
c1.metric("Diagnostics", len(df))
c2.metric("Avg health", f"{df['health_score'].mean():.1f}")
c3.metric("Critical", int((df['severity'] == 'Critical').sum()))

st.write("")
left, right = st.columns(2)

with left:
    st.markdown("#### Health score over time")
    fig = px.line(df, x="timestamp", y="health_score", color="machine", markers=True)
    fig.update_layout(height=340, plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Severity distribution")
    sev = df.groupby("severity").size().reset_index(name="count")
    fig = px.pie(sev, values="count", names="severity", hole=0.55,
                 color="severity",
                 color_discrete_map={"Low": "#16A34A", "Medium": "#F59E0B",
                                     "High": "#EA580C", "Critical": "#DC2626"})
    fig.update_layout(height=340, paper_bgcolor="white",
                      margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Failure analytics")
fa = df.groupby(["machine", "failure"]).size().reset_index(name="count")
fig = px.bar(fa, x="failure", y="count", color="machine", barmode="group")
fig.update_layout(height=360, plot_bgcolor="white", paper_bgcolor="white",
                  margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

with st.expander("Raw diagnostic log"):
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
