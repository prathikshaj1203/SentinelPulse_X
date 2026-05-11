import streamlit as st
from src.ai_assistant import answer
from utils.theme import apply_theme, glass_card

import time
from utils.sidebar import render_sidebar
# Init
st.set_page_config(page_title="Assistant · Sentinel Pulse", layout="wide")
apply_theme()
render_sidebar()

# Header
st.markdown("<h1 style='margin-bottom:0;'>AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B;'>Industrial co-pilot active.</p>", unsafe_allow_html=True)

col_chat, col_info = st.columns([0.7, 0.3])

# Sidebar Stats
with col_info:
    with glass_card("SENTINEL_AI"):
        st.markdown("<div style='text-align:center;'><div style='font-size:3rem;'>🤖</div><h4>Sentinel AI</h4><p style='color:#8B5CF6; font-weight:600; font-size:12px;'>● ONLINE</p></div>", unsafe_allow_html=True)
    
    st.markdown("#### Suggestions")
    samples = ["Why do bearings fail?", "Conveyor belt maintenance", "Motor overheating fix", "Show recent logs"]
    for s in samples:
        if st.button(s, width='stretch'):
            if "chat" not in st.session_state: st.session_state.chat = []
            st.session_state.chat.append({"role": "user", "content": s})
            st.session_state.chat.append({"role": "assistant", "content": answer(s)})
            st.rerun()

# Chat Area
with col_chat:
    if "chat" not in st.session_state:
        st.session_state.chat = [{"role": "assistant", "content": "System initialized. How can I assist today?"}]
    if "last_msg_time" not in st.session_state:
        st.session_state.last_msg_time = 0

    for msg in st.session_state.chat:
        align = "left" if msg["role"] == "assistant" else "right"
        bg = "rgba(255,255,255,0.9)" if msg["role"] == "assistant" else "linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)"
        color = "#1F2937" if msg["role"] == "assistant" else "white"
        st.markdown(f"<div style='display:flex; justify-content:{align}; margin-bottom:1rem;'><div style='background:{bg}; color:{color}; padding:1rem 1.5rem; border-radius:24px; max-width:80% ; box-shadow:0 8px 20px rgba(139, 92, 246, 0.1); border: 1px solid rgba(255,255,255,0.5);'>{msg['content']}</div></div>", unsafe_allow_html=True)

    prompt = st.chat_input("Transmit message...")
    if prompt:
        curr = time.time()
        if curr - st.session_state.last_msg_time < 5:
            st.warning("Rate limit active (5s).")
        else:
            st.session_state.chat.append({"role": "user", "content": prompt})
            st.session_state.last_msg_time = curr
            with st.spinner("AI Processing..."):
                reply = answer(prompt)
                st.session_state.chat.append({"role": "assistant", "content": reply})
            st.rerun()
