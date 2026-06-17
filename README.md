# Deep Agent IT Incident Response

An autonomous IT incident response system built with **LangChain Deep Agents** and **FastAPI**. The system receives alerts via webhook, analyzes them using a multi-subagent pipeline, and returns actionable remediation steps — all without human intervention.

---

## Architecture

```
Monitoring Tool (Datadog, Zabbix, etc.)
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
JSON Response
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
└── webhook.py        # FastAPI webhook server
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MohammadHeydari/Deep-Agent-IT-Incident-Response
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

### Run the webhook server

```bash
uvicorn webhook:server --reload --port 8000
```

### Send a test alert

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
  -d '{"alert": "CPU spike to 100% on prod-db-01 at 14:32 UTC. 500 errors on API gateway."}'
```

### Example response

```json
{
  "status": "processed",
  "conclusion": "1. Monitor CPU usage with your observability tool..."
}
```

### Health check

```bash
curl http://localhost:8000/health
```

---

## Connecting a Real Monitoring Tool

Configure your monitoring tool to send a POST request to `/alert` when an incident is detected.

**Datadog Webhook example:**
```
URL: http://your-server:8000/alert
Method: POST
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
```

---

## How It Works

This project implements the **Deep Agent** pattern from LangChain:

- The **Orchestrator** stays clean and delegates tasks to subagents
- Each **subagent** runs in its own isolated, short-lived loop
- The **harness** automatically manages context window limits
- The agent decides the workflow at runtime based on alert severity

---