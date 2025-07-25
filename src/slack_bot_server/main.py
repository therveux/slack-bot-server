from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

ZAP_WEBHOOK = os.getenv("ZAP_WEBHOOK_URL", "https://hooks.zapier.com/hooks/catch/xxxxx/yyyyy")

@app.post("/slack")
async def slack_handler(request: Request):
    form = await request.form()
    text = form.get("text", "").strip()

    # Forward to Zapier
    requests.post(ZAP_WEBHOOK, json={"command": text})

    return {"text": f"Commande `/trads {text}` bien reçue ✅"}