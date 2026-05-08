import streamlit as st

# Theme Colors
PRIMARY = "#4338CA"
ACCENT = "#8B5CF6"
SECONDARY = "#EC4899"
BG_GRADIENT = "linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 50%, #FAE8FF 100%)"
GLASS_BG = "rgba(255, 255, 255, 0.75)"
GLASS_BORDER = "rgba(255, 255, 255, 0.5)"
TEXT_MAIN = "#1F2937"
TEXT_MUTED = "#6B7280"

CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {{
        background: {BG_GRADIENT} !important;
        background-attachment: fixed !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: {TEXT_MAIN} !important;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stHeader"] {{ display: none !important; }}

    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid {GLASS_BORDER} !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"], .stExpander, .stForm, div[data-testid="stMetric"] {{
        background: {GLASS_BG} !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid {GLASS_BORDER} !important;
        border-radius: 28px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 40px -10px rgba(139, 92, 246, 0.1) !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 20px 50px -10px rgba(139, 92, 246, 0.2) !important;
        border-color: {ACCENT} !important;
    }}

    .sp-title {{
        color: {ACCENT} !important;
        font-size: 0.75rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        margin-bottom: 0.75rem !important;
    }}

    h1, h2, h3, h4 {{
        color: {PRIMARY} !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        font-weight: 800 !important;
        color: {ACCENT} !important;
        font-size: 2.4rem !important;
    }}

    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] {{
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 16px !important;
        border: 1px solid {GLASS_BORDER} !important;
    }}

    div[data-testid="stDataFrame"] {{
        background: transparent !important;
    }}
    div[data-testid="stDataFrame"] div[data-baseweb="table"] {{
        background: {GLASS_BG} !important;
        border-radius: 16px !important;
    }}
    
    div[data-testid="stMetric"] {{
        animation: pulseGlass 6s infinite ease-in-out;
    }}

    .stButton > button {{
        border-radius: 16px !important;
        background: linear-gradient(135deg, {ACCENT} 0%, {SECONDARY} 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px -6px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        box-shadow: 0 12px 25px -6px rgba(139, 92, 246, 0.5) !important;
        transform: scale(1.03) !important;
        color: white !important;
    }}

    #loader-wrapper {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: {BG_GRADIENT};
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOutLoader 0.4s ease-in 0.8s forwards;
        pointer-events: none;
    }}
    
    @keyframes fadeOutLoader {{
        to {{ opacity: 0; visibility: hidden; }}
    }}
    
    .spinner-ui {{
        width: 50px;
        height: 50px;
        border: 5px solid rgba(139, 92, 246, 0.1);
        border-top-color: {ACCENT};
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 15px;
    }}
    
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}

    .block-container {{
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
        opacity: 0;
        animation: fadeInContent 0.3s ease-in 1s forwards;
    }}
    
    @keyframes fadeInContent {{
        to {{ opacity: 1; }}
    }}
</style>

<div id="loader-wrapper">
    <div class="spinner-ui"></div>
    <div style="font-weight:700; color:{PRIMARY}; letter-spacing:0.1em; font-size:12px;">SENTINEL_PULSE_BOOTING...</div>
</div>
"""

# Apply Theme
def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)

# Glass Card Utility
def glass_card(title=None):
    if title:
        st.markdown(f"<div class='sp-title'>{title}</div>", unsafe_allow_html=True)
    return st.container(border=True)

# Status Color Helper
def status_color(score: float) -> tuple[str, str]:
    if score >= 75: return "Optimal", "#8B5CF6"
    if score >= 50: return "Attention", "#EC4899"
    return "Critical", "#EF4444"
