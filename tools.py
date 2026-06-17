from langchain_core.tools import tool
from llm import llm

@tool
def collect_alert(raw_alert: str) -> str:
    """Parse and normalise a raw IT monitoring alert."""
    response = llm.invoke(
        f"Parse this alert and extract: source system, timestamp, "
        f"affected service, error type, impact scope.\n\nAlert: {raw_alert}"
    )
    return response.content

@tool
def screen_alert(alert: str) -> str:
    """Assign severity (LOW/MEDIUM/HIGH/CRITICAL) and urgency to an alert."""
    response = llm.invoke(
        f'Reply in JSON only: {{"severity": "LOW|MEDIUM|HIGH|CRITICAL", '
        f'"urgency": "ROUTINE|URGENT|IMMEDIATE"}}.\n\nAlert: {alert}'
    )
    return response.content

@tool
def analyze_alert(alert: str, severity: str) -> str:
    """Identify the root cause. Only call this for HIGH or CRITICAL severity."""
    response = llm.invoke(
        f"Identify the most likely root cause.\n\nAlert: {alert}\nSeverity: {severity}"
    )
    return response.content

@tool
def fix_incident(root_cause: str, severity: str) -> str:
    """Generate step-by-step remediation steps for the incident."""
    response = llm.invoke(
        f"Provide numbered remediation steps.\n\nRoot cause: {root_cause}\nSeverity: {severity}"
    )
    return response.content

@tool
def escalate(alert: str, reason: str) -> str:
    """Escalate to a human engineer when the agent cannot resolve the incident."""
    return f"ESCALATED: {reason} | Alert: {alert[:100]}"

tools = [collect_alert, screen_alert, analyze_alert, fix_incident, escalate]