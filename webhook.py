from fastapi import FastAPI, Request
from langchain_core.messages import HumanMessage
from main import app as agent_app

server = FastAPI()

@server.post("/alert")
async def receive_alert(request: Request):
    body = await request.json()
    
    raw_alert = body.get("alert") or body.get("message") or str(body)
    
    print(f"\nWebhook received: {raw_alert[:80]}...")

    result = agent_app.invoke({
        "messages": [HumanMessage(content=f"Handle this IT alert: {raw_alert}")]
    })

    final = result["messages"][-1].content
    return {"status": "processed", "conclusion": final}

@server.get("/health")
async def health():
    return {"status": "ok"}