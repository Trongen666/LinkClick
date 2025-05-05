from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from typing import Optional, Dict, Callable

from app.core.config import settings

class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        # Skip auth for certain paths
        if request.url.path.startswith("/api/v1/auth") or request.url.path == "/api/v1/docs":
            return await call_next(request)
        
        # Check for token
        token = self._get_token_from_header(request)
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"}
            )
        
        # Validate token
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                )
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication token"}
            )
        
        # Continue processing the request
        return await call_next(request)
    
    def _get_token_from_header(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return None
        
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            return None
        
        return token