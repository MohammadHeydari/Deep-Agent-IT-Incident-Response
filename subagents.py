from tools import collect_alert, screen_alert, analyze_alert, fix_incident, escalate

collector_subagent = {
    "name": "collector",
    "description": "Parses and normalises raw IT alerts. Call this first with the raw alert text.",
    "tools": [collect_alert],
    "system_prompt": "You are an IT alert ingestion agent. Extract: source system, timestamp, affected service, error type, impact scope.",
}

screener_subagent = {
    "name": "screener",
    "description": "Screens and prioritizes alerts. Call this after collector.",
    "tools": [screen_alert],
    "system_prompt": "You are an IT alert screener. Determine priority level (P1-P4) and whether immediate action is needed.",
}

analyzer_subagent = {
    "name": "analyzer",
    "description": "Analyzes root cause of the incident. Call this after screener.",
    "tools": [analyze_alert],
    "system_prompt": "You are an IT incident analyzer. Identify root cause, affected components, and recommended fix.",
}

fixer_subagent = {
    "name": "fixer",
    "description": "Generates step-by-step remediation actions given a root cause and severity.",
    "tools": [fix_incident, escalate],
    "system_prompt": "Provide numbered, actionable remediation steps.",
}

subagents = [collector_subagent, screener_subagent, analyzer_subagent, fixer_subagent]