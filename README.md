# Deep Agent IT Incident Response

An autonomous IT incident response system built with **LangChain Deep Agents** and **FastAPI**. The system monitors real system resources, sends alerts via webhook, analyzes them using a multi-subagent pipeline, and returns actionable remediation steps — all without human intervention.

Inspired by [this Medium article](https://medium.com/) on Deep Agents for IT operations.

---

## Architecture

```
monitor.py (psutil)
  reads real system metrics
        ↓
POST /alert  (FastAPI Webhook)
        ↓
┌─────────────────────────────┐
│        Deep Agent           │
│                             │
│  collector  → normalize     │
│  screener   → severity      │
│  analyzer   → root cause    │
│  fixer      → remediation   │
└─────────────────────────────┘
        ↓
JSON Response + Console Output
```

### Subagents

| Subagent | Responsibility |
|----------|---------------|
| **Collector** | Parses and normalizes raw alerts |
| **Screener** | Assigns severity (LOW/MEDIUM/HIGH/CRITICAL) and urgency |
| **Analyzer** | Identifies root cause (HIGH/CRITICAL only) |
| **Fixer** | Generates step-by-step remediation actions or escalates |

---

## Project Structure

```
deep-agent-it-incident-response/
├── .env              # API keys (not committed)
├── .gitignore
├── requirements.txt
├── llm.py            # LLM client setup
├── tools.py          # LangChain tools
├── subagents.py      # Subagent definitions
├── main.py           # Deep agent orchestrator
├── webhook.py        # FastAPI webhook server
└── monitor.py        # Real-time system monitor (psutil)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mohammadheydari/deep-agent-it-incident-response.git
cd deep-agent-it-incident-response
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
AVVALAI_API_KEY=your-api-key
AVVALAI_BASE_URL=https://api.avalai.ir/v1
AVVALAI_MODEL=gpt-4o-mini
```

> Works with any OpenAI-compatible API (OpenAI, Avval AI, Azure OpenAI, etc.)

---

## Usage

### Step 1 — Start the webhook server

```bash
uvicorn webhook:server --reload --port 8000
```

### Step 2 — Start the system monitor

Open a second terminal and run:

```bash
python monitor.py
```

The monitor will read real metrics from your machine every 10 seconds and automatically send alerts to the webhook when thresholds are exceeded.

### Default thresholds

```python
THRESHOLDS = {
    "cpu":  90,   # CPU usage %
    "ram":  85,   # RAM usage %
    "disk": 95,   # Disk usage %
    "gpu":  90,   # GPU usage %
}
```

### Example output

```
Monitoring started. Checking every 10s...
Thresholds: CPU>90% | RAM>85% | Disk>95%

[ALERT] Disk usage at 96.5% on MyPC at 07:48 UTC. Free: 11.5GB of 328.3GB.
[AGENT] To address the high disk usage on C:\, follow these remediation steps:
1. Run Disk Cleanup...
2. Identify large files...
```

---

## Manual Testing

Send a test alert without the monitor:

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/alert" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"alert": "CPU spike to 100% on prod-db-01 at 14:32 UTC. 500 errors on API gateway."}'
```

**curl:**
```bash
curl -X POST http://localhost:8000/alert \
  -H "Content-Type: application/json" \
  -d '{"alert": "CPU spike to 100% on prod-db-01 at 14:32 UTC."}'
```

### Health check

```bash
curl http://localhost:8000/health
```

---

## Connecting an External Monitoring Tool

You can also connect external tools like Datadog or Zabbix by pointing their webhook to `/alert`:

```
URL:     http://your-server:8000/alert
Method:  POST
Payload: {"alert": "$EVENT_TITLE - $EVENT_MSG"}
```

---

## Requirements

```
langchain
langgraph
deepagents
langchain-openai
fastapi
uvicorn
python-dotenv
psutil
requests
gputil
```

---

## How It Works

This project implements the **Deep Agent** pattern from LangChain:

- The **Orchestrator** stays clean and delegates tasks to subagents
- Each **subagent** runs in its own isolated, short-lived loop
- The **harness** automatically manages context window limits
- The agent decides the workflow at runtime based on alert severity
- `monitor.py` reads **real system metrics** using `psutil` — no external monitoring tool needed
