"""Batch CSV Inference — upload a CSV of sensor readings, get predictions."""

import sys
from pathlib import Path
from utils.sidebar import render_sidebar
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import io
import pandas as pd
import plotly.express as px
import streamlit as st

from src.inference import FailurePredictor
from utils.theme import apply_theme

st.set_page_config(
    page_title="Batch Inference · Sentinel Pulse",
    layout="wide"
)

apply_theme()
render_sidebar()

st.markdown("### Batch CSV Inference")

st.markdown(
    "<div class='sp-muted'>Upload sensor readings as CSV — get failure probability and predicted failure category for each row.</div>",
    unsafe_allow_html=True
)

st.write("")

try:

    predictor = FailurePredictor()

except FileNotFoundError:

    st.error(
        "No trained model found. Run `python src/train_model.py` first."
    )

    st.stop()

st.markdown(
    f"**Required columns:** `{', '.join(predictor.features)}`"
)

st.caption(
    f"Model: failure-prob + category classifier · Classes: {', '.join(predictor.meta.get('classes', [])) or 'n/a'}"
)

uploaded = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

use_sample = st.checkbox(
    "Use bundled sample dataset instead"
)

if uploaded is None and not use_sample:

    st.info(
        "Upload a CSV or tick the sample option to run predictions."
    )

    st.stop()

if use_sample:

    df = pd.read_csv(

        Path(__file__).resolve().parent.parent
        / "datasets"
        / "predictive_maintenance.csv"

    ).head(200)

else:

    df = pd.read_csv(uploaded)

st.markdown("#### Input preview")

st.dataframe(
    df.head(10),
    width='stretch',
    hide_index=True
)

try:

    pred = predictor.predict(df)

except ValueError as e:

    st.error(str(e))

    st.stop()

result = pd.concat(
    [df.reset_index(drop=True), pred],
    axis=1
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Rows scored",
    len(result)
)

c2.metric(
    "Predicted failures",
    int((result["failure_probability"] >= 0.5).sum())
)

c3.metric(
    "Avg health score",
    f"{result['health_score'].mean():.1f}"
)

st.markdown("#### Failure-probability distribution")

fig = px.histogram(

    result,

    x="failure_probability",

    nbins=30,

    color="predicted_category"
)

fig.update_layout(

    height=320,

    plot_bgcolor="white",

    paper_bgcolor="white",

    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    )
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.markdown("#### Predictions")

st.dataframe(
    result,
    width='stretch',
    hide_index=True
)

buf = io.StringIO()

result.to_csv(
    buf,
    index=False
)

st.download_button(
    "Download predictions CSV",
    buf.getvalue(),
    file_name="sentinel_pulse_predictions.csv",
    mime="text/csv"
)