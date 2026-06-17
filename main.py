from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_core.messages import HumanMessage
from llm import llm
from subagents import (
    collector_subagent,
    screener_subagent,
    analyzer_subagent,
    fixer_subagent,
)

app = create_deep_agent(
    model=llm,
    subagents=[collector_subagent, screener_subagent, analyzer_subagent, fixer_subagent],
    system_prompt="""You are an autonomous IT incident management agent.
                    When given an alert:
                    1. Use collector to normalise it
                    2. Use screener to determine severity and urgency
                    3. If HIGH or CRITICAL → use analyzer, then fixer
                    4. If LOW or MEDIUM → use fixer directly
                    5. If root cause is unclear after analysis → escalate
                    Never fabricate information.""",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True)
)

ALERTS = [
    "CPU spike to 100% on prod-db-02 at 00:32 UTC. 500 errors on API gateway.",
    "Disk usage at 99% on prod-storage-03. Write latency > 900ms.",
]

def process_alert(raw_alert: str):
    print(f"\n{'='*60}")
    print(f"Processing: {raw_alert[:60]}...")
    print('='*60)

    result = app.invoke({
        "messages": [HumanMessage(content=f"Handle this IT alert: {raw_alert}")]
    })

    final = result["messages"][-1].content
    print(f"\nAgent conclusion:\n{final}")

    print(f"\n--- FULL TRACE ---")
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content:
            print(f"\n[{type(msg).__name__}]: {msg.content[:200]}")

if __name__ == "__main__":
    for alert in ALERTS:
        process_alert(alert)