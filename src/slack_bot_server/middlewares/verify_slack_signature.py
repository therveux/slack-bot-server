import hashlib
import hmac
import os
import time
from functools import wraps

from fastapi import HTTPException, Request

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

def verify_slack_signature(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Skip signature check if DEBUG env var is set to true
        if os.getenv("DEBUG", "false").lower() == "true":
            return await func(request, *args, **kwargs)

        # https://api.slack.com/authentication/verifying-requests-from-slack#:~:text=Understanding%20signed%20secrets&text=The%20signature%20is%20created%20by,information%2C%20keeping%20your%20app%20secure.
        timestamp = request.headers.get("X-Slack-Request-Timestamp")
        slack_signature = request.headers.get("X-Slack-Signature")

        if not timestamp or not slack_signature:
            raise HTTPException(status_code=400, detail="Missing Slack signature headers")

        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > 60 * 5:
            raise HTTPException(status_code=400, detail="Request timestamp out of range")

        body = await request.body()
        sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
        computed_signature = "v0=" + hmac.new(
            SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed_signature, slack_signature):
            raise HTTPException(status_code=403, detail="Invalid Slack signature")

        return await func(request, *args, **kwargs)
    return wrapper