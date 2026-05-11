"""Health Reports — analytics over diagnostic history."""

import sys
from pathlib import Path
from utils.sidebar import render_sidebar
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.theme import apply_theme
from database.db import fetch_predictions

st.set_page_config(
    page_title="Health Reports · Sentinel Pulse",
    layout="wide"
)

apply_theme()
render_sidebar()

st.markdown("### Health Reports")

st.markdown(
    "<div class='sp-muted'>Diagnostic history, severity distribution, and maintenance trends.</div>",
    unsafe_allow_html=True
)

st.write("")

df = fetch_predictions()

if df.empty:

    st.info("No diagnostic data yet. Run a few diagnoses first.")

    st.stop()

df["created_at"] = pd.to_datetime(df["created_at"])

df = df.sort_values("created_at")

# ---------------- METRICS ---------------- #

c1, c2, c3 = st.columns(3)

c1.metric(
    "Diagnostics",
    len(df)
)

c2.metric(
    "Avg Risk Score",
    f"{df['risk_score'].mean():.1f}"
)

c3.metric(
    "Critical",
    int((df['status'] == 'Critical').sum())
)

st.write("")

left, right = st.columns(2)

# ---------------- LINE CHART ---------------- #

with left:

    st.markdown("#### Risk score over time")

    fig = px.line(

        df,

        x="created_at",
        y="risk_score",

        markers=True
    )

    fig.update_layout(

        height=340,

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

# ---------------- STATUS DISTRIBUTION ---------------- #

with right:

    st.markdown("#### Status distribution")

    sev = df.groupby(
        "status"
    ).size().reset_index(name="count")

    fig = px.pie(

        sev,

        values="count",
        names="status",

        hole=0.55,

        color="status",

        color_discrete_map={

            "Healthy": "#16A34A",

            "Warning": "#F59E0B",

            "Critical": "#DC2626"
        }
    )

    fig.update_layout(

        height=340,

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

# ---------------- SENSOR ANALYTICS ---------------- #

st.markdown("#### Sensor analytics")

fig = px.bar(

    df,

    x="id",
    y=["temperature", "vibration", "pressure"],

    barmode="group"
)

fig.update_layout(

    height=360,

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

# ---------------- RAW DATA ---------------- #

with st.expander("Raw PostgreSQL records"):

    st.dataframe(
        df.iloc[::-1],
        width='stretch',
        hide_index=True
    )