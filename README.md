````markdown
# SentinelPulse_X
### AI-Powered Predictive Maintenance System

SentinelPulse_X is an AI-powered predictive maintenance platform designed for automotive and industrial environments. The system uses Random Forest Machine Learning models and Google Gemini AI to analyze machine conditions, detect possible failures, generate health reports, and provide intelligent maintenance recommendations.

---

## Features

- Machine Failure Prediction
- Health Score Generation
- AI Assistant Integration
- Batch CSV Inference
- Machine Intelligence Base
- Diagnostic Logging System
- Interactive Streamlit Dashboard
- PostgreSQL Database Integration
- Predictive Analytics Workflow

---

## Tech Stack

- Python
- Streamlit
- PostgreSQL
- Scikit-learn
- Pandas
- Google Gemini AI
- Joblib
- Git & GitHub

---

## Project Structure

```bash
SentinelPulse_X/
└── sentinel_pulse/
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── .env
    │
    ├── database/
    │   └── db.py
    │
    ├── datasets/
    │   └── predictive_maintenance.csv
    │
    ├── knowledge_base/
    │   └── machines.json
    │
    ├── logs/
    │   ├── diagnostics.csv
    │   └── system.csv
    │
    ├── models/
    │   ├── rf_model.joblib
    │   ├── rf_failure_class.joblib
    │   ├── rf_failure_prob.joblib
    │   ├── model_meta.json
    │   └── rf_meta.json
    │
    ├── pages/
    │   ├── 1_Machine_Diagnosis.py
    │   ├── 2_Health_Reports.py
    │   ├── 3_AI_Assistant.py
    │   ├── 4_Machine_Intelligence_Base.py
    │   ├── 5_System_Logs.py
    │   └── 6_Batch_CSV_Inference.py
    │
    ├── src/
    │   ├── ai_assistant.py
    │   ├── diagnostic_engine.py
    │   ├── inference.py
    │   └── train_model.py
    │
    ├── utils/
    │   ├── kb_loader.py
    │   ├── logger.py
    │   ├── sidebar.py
    │   └── theme.py
    │
    └── scratch/
        └── list_models.py
````

---

## Core Modules

| Module               | Purpose                                  |
| -------------------- | ---------------------------------------- |
| diagnostic_engine.py | Machine diagnostics and failure analysis |
| inference.py         | ML prediction workflow                   |
| train_model.py       | Random Forest model training             |
| ai_assistant.py      | Gemini AI integration                    |
| db.py                | PostgreSQL database operations           |
| kb_loader.py         | Knowledge base management                |
| logger.py            | System and diagnostic logging            |

---

## ML Models Used

* Random Forest Classifier
* Failure Probability Prediction Model
* Failure Classification Model

---

## Workflow

```text
User Input
↓
Machine Identification
↓
Symptom / Sensor Analysis
↓
Knowledge Base Matching
↓
ML Prediction
↓
Failure Detection
↓
Health Score Generation
↓
Maintenance Recommendations
↓
AI Assistant Guidance
↓
Dashboard Visualization
```

---

## Current Modules Implemented

* Machine Diagnosis System
* Health Reports Dashboard
* AI Assistant
* Machine Intelligence Base
* System Logs Management
* Batch CSV Inference
* PostgreSQL Data Storage
* Predictive Maintenance Workflow

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd SentinelPulse_X
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key

DB_HOST=localhost
DB_NAME=sentinel_pulse
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

---

## Future Improvements

* Real-time IoT Sensor Integration
* Advanced ML Models
* Cloud Deployment
* Real-time Alerts & Notifications
* Automated Maintenance Reports
* Continuous Model Training
* Multi-Industry Expansion
* Enhanced AI Assistant Features

---

## Developed By

**PRATHIKSHA J**
Department of IT & Cognitive Systems
Sri Krishna Arts & Science College

```
```
