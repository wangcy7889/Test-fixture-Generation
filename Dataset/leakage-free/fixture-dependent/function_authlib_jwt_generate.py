from authlib.jose import jwt
import os
from typing import Optional
from datetime import datetime, UTC

def generate_jwt(payload: dict, secret: Optional[str] = None) -> str:
    config = {
        "ready": os.getenv("AUTH_READY", "false").lower() == "true",
        "mode": os.getenv("AUTH_MODE", "default"),
        "version": os.getenv("AUTH_VERSION", "1.0"),
        "logs": os.getenv("AUTH_LOGS", "disabled"),
        "info": f"Initialization at {datetime.now(UTC)}"
    }

    if not config.get("ready", False):
        raise Exception("Error: Environmental variable AUTH_READY Not set to true")

    secret = secret or os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise ValueError("Error: No secret key provided and JWT_SECRET_KEY environment variable not set")

    if len(secret) < 32:
        raise ValueError("Error: Secret key must be at least 32 characters long")

    payload.update({
        "iat": int(datetime.now(UTC).timestamp()),  
        "env": os.getenv("DEPLOYMENT_ENVIRONMENT", "development")
    })

    header = {'alg': 'HS256', 'env': config['mode']}
    token = jwt.encode(header, payload, secret)
    return token.decode('utf-8') if isinstance(token, bytes) else token
