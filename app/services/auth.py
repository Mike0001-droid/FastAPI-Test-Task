from typing import Optional
from fastapi import HTTPException, Header
from app.config.config import SECRET_API_KEY



async def verify_api_key(x_api_key: Optional[str] = Header(None, include_in_schema=False)):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is required. Use X-API-Key header"
        )
    
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return x_api_key