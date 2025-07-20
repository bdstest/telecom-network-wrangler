from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional

security = HTTPBearer()

class SecurityManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        '''Verify JWT token for API authentication'''
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            username = payload.get('sub')
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid authentication token'
                )
            return username
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication token'
            )
    
    def check_permissions(self, required_permission: str, user_permissions: list):
        '''Check if user has required permissions for network operations'''
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Insufficient permissions: {required_permission} required'
            )
        return True
from fastapi import Request, HTTPException
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> bool:
        '''Check if request is allowed based on rate limits'''
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > window_start
        ]
        
        # Check if within limits
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_ip].append(now)
        return True

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    '''Rate limiting middleware for API protection'''
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail='Rate limit exceeded. Please try again later.'
        )
    
    response = await call_next(request)
    return response
