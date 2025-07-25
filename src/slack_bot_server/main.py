import os
from enum import Enum

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

from slack_bot_server.middlewares.validate_env import require_env_vars
from slack_bot_server.middlewares.verify_slack_signature import \
    verify_slack_signature

load_dotenv()

app = FastAPI()

ZAP_WEBHOOK = os.getenv("ZAP_WEBHOOK_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WORKFLOW_MISSING = os.getenv("GITHUB_MISSING_TRADS_WORKFLOW_URL")

class TradOption(str, Enum):
    missing = "missing"
    unused = "unused"

WORKFLOW_MAP = {
    TradOption.missing: WORKFLOW_MISSING,
    TradOption.unused: "unused.yml"
}

@app.post("/trads")
@verify_slack_signature
@require_env_vars("GITHUB_TOKEN", "GITHUB_MISSING_TRADS_WORKFLOW_URL")
async def slack_handler(request: Request):
    form = await request.form()
    option_text = form.get("text", "").strip()

    try:
        option = TradOption(option_text)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid option '{option_text}'")

    workflow_url = WORKFLOW_MAP.get(option)
    if not workflow_url:
        raise HTTPException(status_code=400, detail="No workflow configured for this option")

    print(f"workflow url '{workflow_url}'")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    json_data = {
        "ref": "develop"
    }

    resp = requests.post(workflow_url, headers=headers, json=json_data)

    print("Status code:", resp.status_code)
    print("Response text:", resp.text)

    if resp.status_code != 204:
        raise HTTPException(status_code=resp.status_code, detail=f"GitHub API error: {resp.text}")

    return {"message": f"Triggered GitHub Action '{workflow_url}' for option '{option.value}' successfully."}