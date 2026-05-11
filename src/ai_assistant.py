import pandas as pd
import google.generativeai as genai
from utils.logger import DIAG_LOG, read_log
from utils.kb_loader import list_machines
import os


# API Config
GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# AI Prompt
SYSTEM_PROMPT = """You are the Sentinel Pulse AI Assistant. 
Purpose: Industrial maintenance and machinery diagnosis.
Machines: {machines}
Rule: Decline off-topic chat. No AI for logs."""

# AI Response Logic
def answer(prompt: str) -> str:
    p_lower = prompt.lower()
    
    # Log Retrieval Fallback
    if any(k in p_lower for k in ["recent logs", "history", "past diagnostics", "last logs"]):
        try:
            df = read_log(DIAG_LOG).tail(5).iloc[::-1]
            if df.empty: return "No recent diagnostics found."
            
            log_str = "📋 **RECENT LOGS:**\n\n"
            for _, row in df.iterrows():
                log_str += f"- **{row['machine']}**: {row['failure']} ({row['severity']}) | {row['health_score']}%\n"
            return log_str
        except: return "Error retrieving logs."

    # Gemini AI logic
    try:
        m_list = ", ".join([m["machine_name"] for m in list_machines()])
        full_prompt = f"{SYSTEM_PROMPT.format(machines=m_list)}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"AI_ERROR: {str(e)}"
