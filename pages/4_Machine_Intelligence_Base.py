import streamlit as st
from utils.kb_loader import list_machines
from utils.theme import apply_theme, glass_card
from utils.sidebar import render_sidebar
# Init
st.set_page_config(
    page_title="Knowledge Base · Sentinel Pulse",
    layout="wide"
)

apply_theme()
render_sidebar()

st.markdown("### Machine Intelligence Base")

st.write("")

# DB List
machines = list_machines()

search = st.text_input(
    "Filter database...",
    placeholder="Search machine name..."
)

for m in machines:

    if search and search.lower() not in m["machine_name"].lower():

        continue

    with st.expander(
        f"📁 {m['machine_name'].upper()}",
        expanded=False
    ):

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Components",
            len(m["components"])
        )

        c2.metric(
            "Failure Modes",
            len(m["common_failures"])
        )

        c3.metric(
            "Aliases",
            len(m["aliases"])
        )

        st.markdown("---")

        col_l, col_r = st.columns(2)

        with col_l:

            with glass_card("BLUEPRINT.SYS"):

                st.markdown(

                    f"""
                    <div style='font-size:13px;'>

                        <b>Components:</b>

                        <br>

                        {', '.join(m['components'])}

                        <br><br>

                        <b>Aliases:</b>

                        <br>

                        {', '.join(m['aliases'])}

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        with col_r:

            rows = "".join([

                f"<li>{f['name']} ({f['severity']})</li>"

                for f in m["common_failures"]

            ])

            with glass_card("RISK_MATRIX.LOG"):

                st.markdown(

                    f"""
                    <ul style='font-size:12px; margin-left:-20px;'>

                        {rows}

                    </ul>
                    """,

                    unsafe_allow_html=True
                )

        st.markdown("##### 🛠️ Maintenance Playbook")

        if "recommendations" in m and m["recommendations"]:

            for fname, recs in m["recommendations"].items():

                st.info(
                    f"**{fname}**: " + " · ".join(recs)
                )

        else:

            st.info(
                "General maintenance protocols apply."
            )