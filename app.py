import streamlit as st
import pandas as pd
import plotly.express as px
from utils.theme import apply_theme, status_color, ACCENT, glass_card
from utils.kb_loader import list_machines
from utils.logger import DIAG_LOG, read_log, log_system

# Init
st.set_page_config(page_title="Sentinel Pulse", page_icon="📡", layout="wide")
apply_theme()
log_system("dashboard_view")

# Header
col_h1, col_h2 = st.columns([0.7, 0.3])
with col_h1:
    st.markdown("<p style='color:#64748B; font-weight:600; margin-bottom:0;'>Welcome back, Operator 👋</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top:0; font-size:2.5rem;'>Dashboard</h1>", unsafe_allow_html=True)

# Data
machines = list_machines()
df_log = read_log(DIAG_LOG)
total_diag = len(df_log)
total_failures = int((df_log["severity"].isin(["High", "Critical"])).sum()) if total_diag else 0
avg_health = round(df_log["health_score"].mean(), 1) if total_diag else 100.0

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
            df_log["status"] = df_log["health_score"].apply(lambda s: status_color(s)[0])
            agg = df_log.groupby("status").size().reset_index(name="count")
            fig = px.pie(agg, values="count", names="status", hole=0.6,
                         color="status", color_discrete_map={"Optimal": "#8B5CF6", "Attention": "#EC4899", "Critical": "#EF4444"})
            fig.update_layout(showlegend=True, height=350, margin=dict(l=10, r=10, t=10, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(family="Plus Jakarta Sans", color="#4338CA"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("<p style='text-align:center; padding:40px; color:#64748B;'>No diagnostic data available.</p>", unsafe_allow_html=True)

# Sidebar Alerts
with col_side:
    st.markdown("#### System Alerts")
    if total_failures > 0:
        critical_logs = df_log[df_log["severity"].isin(["High", "Critical"])].tail(5).iloc[::-1]
        for _, row in critical_logs.iterrows():
            content = f"<div style='margin-bottom:12px;'><b>{row['machine']}</b><br><span style='color:#DC2626; font-size:12px;'>⚠️ {row['failure']}</span></div>"
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
    st.dataframe(df_log.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("Audit trail is empty.")
