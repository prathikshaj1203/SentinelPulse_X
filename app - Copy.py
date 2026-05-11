import streamlit as st
import plotly.express as px
from utils.theme import apply_theme
from utils.kb_loader import list_machines
from utils.sidebar import render_sidebar
from database.db import (
    create_tables,
    create_system_logs_table,
    fetch_predictions
)

# Init
st.set_page_config(page_title="Sentinel Pulse", page_icon="📡", layout="wide")
create_tables()
create_system_logs_table()
apply_theme()


st.markdown("""
<style>

/* HIDE DEFAULT STREAMLIT NAVIGATION */
section[data-testid="stSidebarNav"] {
    display: none !important;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f5f3ff 100%
    ) !important;

    border-right: 1px solid rgba(139,92,246,0.08);

    width: 280px !important;
    min-width: 280px !important;

    box-shadow: 8px 0 30px rgba(139,92,246,0.06);

    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)
render_sidebar()

# Header
col_h1, col_h2 = st.columns([0.7, 0.3])
with col_h1:
    st.markdown("<p style='color:#64748B; font-weight:600; margin-bottom:0;'>Welcome back, Operator 👋</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top:0; font-size:2.5rem;'>Dashboard</h1>", unsafe_allow_html=True)

# Data
machines = list_machines()
df_log = fetch_predictions()
total_diag = len(df_log)
total_failures = (
    int((df_log["status"] == "Critical").sum())
    if total_diag and "status" in df_log.columns
    else 0
)
avg_health = (
    round(df_log["risk_score"].mean(), 1)
    if total_diag and "risk_score" in df_log.columns
    else 100.0
)
col_main, col_side = st.columns([0.65, 0.35])

# Main Dashboard
with col_main:
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("<div class='sp-title'>Fleet Status</div>", unsafe_allow_html=True)
            st.markdown(f"<h2>{len(machines)}</h2><p style='color:#64748B; font-size:14px;'>Active Assets</p>", unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown("<div class='sp-title'>System Activity</div>", unsafe_allow_html=True)
            st.markdown(f"<h2>{total_diag}</h2><p style='color:#64748B; font-size:14px;'>Total Diagnostics</p>", unsafe_allow_html=True)
    with c3:
        color = "#8B5CF6" if avg_health > 80 else "#EC4899"
        with st.container(border=True):
            st.markdown("<div class='sp-title'>Fleet Health</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:{color};'>{avg_health}%</h2><p style='color:#64748B; font-size:14px;'>Avg Health Score</p>", unsafe_allow_html=True)

    st.markdown("#### Diagnostic Overview")
    with st.container(border=True):
        st.markdown("<div class='sp-title'>HEALTH_DISTRIBUTION</div>", unsafe_allow_html=True)
        if total_diag:
            agg = df_log.groupby("status").size().reset_index(name="count")
            fig = px.pie(
    agg,
    values="count",
    names="status",
    hole=0.6,
    color="status",
    color_discrete_map={
        "Healthy": "#8B5CF6",
        "Warning": "#EC4899",
        "Critical": "#EF4444"
    }
)
            fig.update_layout(showlegend=True, height=350, margin=dict(l=10, r=10, t=10, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(family="Plus Jakarta Sans", color="#4338CA"))
            st.plotly_chart(fig, width='stretch')
        else:
            st.markdown("<p style='text-align:center; padding:40px; color:#64748B;'>No diagnostic data available.</p>", unsafe_allow_html=True)

# Sidebar Alerts
with col_side:
    st.markdown("#### System Alerts")
    if total_failures > 0:
        critical_logs = df_log[df_log["status"] == "Critical"].tail(5).iloc[::-1]
        for _, row in critical_logs.iterrows():
            content = f"<div style='margin-bottom:12px;'><b>Critical Machine Alert</b><br><span style='color:#DC2626; font-size:12px;'>⚠️ Risk Score: {row['risk_score']}</span></div>"
            st.markdown(f"<div style='background:rgba(220, 38, 38, 0.05); border-radius:12px; padding:12px; margin-bottom:10px; border-left:4px solid #DC2626;'>{content}</div>", unsafe_allow_html=True)
    else:
        st.success("No critical alerts detected.")
    
    st.write("")
    st.markdown("#### Machine Registry")
    with st.container(border=True):
        st.markdown("<div class='sp-title'>NODES</div>", unsafe_allow_html=True)
        rows = ""
        for m in machines:
            rows += f"<div style='padding:10px 0; border-bottom:1px solid rgba(0,0,0,0.05);'><b>{m['machine_name']}</b><br><small style='color:#64748B;'>{len(m['components'])} components</small></div>"
        st.markdown(f"<div style='max-height:280px; overflow-y:auto;'>{rows}</div>", unsafe_allow_html=True)

# Audit Log
st.markdown("#### Recent Activity Log")
if total_diag:
    st.dataframe(df_log.tail(10).iloc[::-1], width='stretch', hide_index=True)
else:
    st.info("Audit trail is empty.")

