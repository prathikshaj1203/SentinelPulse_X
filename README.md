# Sentinel Pulse

AI-powered industrial diagnostic platform for the automotive industry.
Built with **Python + Streamlit + scikit-learn + Plotly**.

## Run locally

```bash
pip install -r requirements.txt
python src/train_model.py        # trains and saves the ML model (one-time)
streamlit run app.py
```

## Project structure

```
sentinel_pulse/
├── app.py                       # Entry / Dashboard
├── pages/                       # Streamlit multipage app
│   ├── 1_Machine_Diagnosis.py
│   ├── 2_Health_Reports.py
│   ├── 3_AI_Assistant.py
│   ├── 4_Machine_Intelligence_Base.py
│   └── 5_System_Logs.py
├── knowledge_base/machines.json # Machine intelligence DB
├── src/                         # ML + diagnostic engine
│   ├── train_model.py
│   ├── diagnostic_engine.py
│   └── ai_assistant.py
├── utils/                       # Shared helpers
│   ├── kb_loader.py
│   ├── theme.py
│   └── logger.py
├── datasets/                    # Synthetic training data (auto-generated)
├── models/                      # Saved scikit-learn model
└── logs/                        # Diagnostic + system logs
```

## Supported machines

- Industrial Motor
- Conveyor System
- Air Compressor

Add more by appending to `knowledge_base/machines.json`.
