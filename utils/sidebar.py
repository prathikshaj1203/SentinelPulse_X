import streamlit as st

def render_sidebar():
    print("Rendering sidebar...")
    st.markdown("""
<style>

/* FIX SIDEBAR */
section[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0;
    left: 0;
    height: 100vh;
    overflow-y: auto;
    z-index: 999999;

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

/* HIDE DEFAULT STREAMLIT NAV */
[data-testid="stSidebarNav"] {
    display: none;
}

/* PUSH MAIN CONTENT */
[data-testid="stAppViewContainer"] {
    margin-left: 280px;
}

                
/* SIDEBAR CONTENT */
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* BUTTONS */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 12px 14px;
    text-align: left;

    background: linear-gradient(
        135deg,
        #8B5CF6 0%,
        #EC4899 100%
    );

    color: white;

    font-weight: 600;
    font-size: 15px;

    margin-bottom: 12px;

    transition: all 0.2s ease;

    box-shadow: 0 8px 20px rgba(139,92,246,0.18);
}

/* BUTTON HOVER */
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    opacity: 0.92;
}

/* TITLE */
.sidebar-title {
    font-size: 28px;
    font-weight: 800;
    color: #4338CA;
    padding-left: 10px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)
    
    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-title">
                📡 Sentinel Pulse
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("📊 Dashboard", width='stretch'):
            st.switch_page("app.py")

        if st.button("🩺 Machine Diagnosis", width='stretch'):
            st.switch_page("pages/1_Machine_Diagnosis.py")

        if st.button("📈 Health Reports", width='stretch'):
            st.switch_page("pages/2_Health_Reports.py")

        if st.button("🤖 AI Assistant", width='stretch'):
            st.switch_page("pages/3_AI_Assistant.py")

        if st.button("🧠 Intelligence Base", width='stretch'):
            st.switch_page("pages/4_Machine_Intelligence_Base.py")

        if st.button("📜 System Logs", width='stretch'):
            st.switch_page("pages/5_System_Logs.py")

        if st.button("📂 Batch CSV Inference", width='stretch'):
            st.switch_page("pages/6_Batch_CSV_Inference.py")