from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM
import time

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['exp'] < time.time():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

async def validate_ws_token(request: Request):
    """WebSocket专用鉴权"""
    token = request.query_params.get("token")
    if not token:
        raise HTTPException(status_code=403, detail="Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['room_id']
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
