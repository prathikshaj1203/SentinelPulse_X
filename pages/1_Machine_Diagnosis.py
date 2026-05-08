import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
import streamlit as st
from src.diagnostic_engine import DiagnosticEngine
from utils.kb_loader import resolve_machine, list_machines
from utils.theme import apply_theme, status_color
from utils.logger import log_diagnostic, log_system

# Page Config
st.set_page_config(page_title="Diagnosis · Sentinel Pulse", layout="wide")
apply_theme()
log_system("diagnosis_view")

st.markdown("### Machine Diagnosis")
st.markdown("<p style='color:#6B7280;'>Input symptoms to run AI diagnosis.</p>", unsafe_allow_html=True)

# Search Logic
known = [m["machine_name"] for m in list_machines()]
query = st.text_input("Machine name", placeholder="e.g. ac motor, pump, fan")
if not query:
    st.caption("Try: " + " · ".join(known))
    st.stop()

machine = resolve_machine(query)
if not machine:
    st.warning(f"No machine matched '{query}'.")
    st.stop()

st.success(f"Selected: **{machine['machine_name']}**")

# Input Form
answers: dict[str, bool] = {}
with st.form("symptoms"):
    cols = st.columns(2)
    for i, q in enumerate(machine["questions"]):
        with cols[i % 2]:
            answers[q["id"]] = st.checkbox(q["text"], key=f"q_{q['id']}")

    st.markdown("##### Sensor Data")
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    sensors = {
        "vibration":   s1.number_input("Vibration", 0.0, 30.0, 3.0),
        "temperature": s2.number_input("Temp", 0.0, 200.0, 60.0),
        "noise":       s3.number_input("Noise", 0.0, 150.0, 65.0),
        "current":     s4.number_input("Current", 0.0, 100.0, 11.0),
        "rpm":         s5.number_input("RPM", 0.0, 5000.0, 1470.0),
        "pressure":    s6.number_input("Pressure", 0.0, 20.0, 6.0),
    }
    submitted = st.form_submit_button("RUN DIAGNOSIS", type="primary")

if not submitted: st.stop()

# Execution
engine = DiagnosticEngine()
result = engine.diagnose(machine, answers, sensors)
label, color = status_color(result["health_score"])
log_diagnostic(machine["machine_name"], result["top_failure"], result["severity"], result["health_score"])

# Results UI
a, b, c = st.columns([0.4, 0.3, 0.3])
with a:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["health_score"],
        number={"suffix": " / 100", "font": {"size": 26, "family": "Plus Jakarta Sans", "color": "#8B5CF6"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 50], "color": "rgba(239, 68, 68, 0.1)"},
                {"range": [50, 75], "color": "rgba(236, 72, 153, 0.1)"},
                {"range": [75, 100], "color": "rgba(139, 92, 246, 0.1)"},
            ],
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with b:
    st.markdown(f"<div class='sp-card'><div class='sp-title'>Inference</div><h4 style='color:#8B5CF6;'>{result['top_failure']}</h4><p style='font-size:12px; color:#6B7280;'>Sev: {result['severity']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sp-card'><div class='sp-title'>ML Prediction</div><h4 style='color:#EC4899;'>{result['ml_class']}</h4><p style='font-size:12px; color:#6B7280;'>Conf: {result['ml_confidence']*100:.1f}%</p></div>", unsafe_allow_html=True)

with c:
    recs = "".join(f"• {r}<br>" for r in result["recommendations"]) if result["recommendations"] else "Monitor normally."
    st.markdown(f"##### Action Items")
    st.markdown(f"<div class='sp-card' style='font-size:12px;'>{recs}</div>", unsafe_allow_html=True)

# Breakdown
import pandas as pd
import plotly.express as px
breakdown = pd.DataFrame([{"failure": k, "score": v} for k, v in result["per_failure_scores"].items()]).sort_values("score")
fig2 = px.bar(breakdown, x="score", y="failure", orientation="h", color="score", color_continuous_scale=["#8B5CF6", "#EC4899", "#EF4444"])
fig2.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)
