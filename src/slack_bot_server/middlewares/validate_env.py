import os
from functools import wraps

from fastapi import HTTPException


def require_env_vars(*vars):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            missing = [v for v in vars if not os.getenv(v)]
            if missing:
                raise HTTPException(status_code=500, detail=f"Missing env vars: {', '.join(missing)}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator