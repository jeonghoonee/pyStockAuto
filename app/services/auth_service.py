"""
Authentication Service

Business logic for authentication and authorization.
Converted from Kotlin auth services.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models import AuthInfo
import logging
import base64
import json
import httpx
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication-related business logic"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def get_auth_info(self) -> Optional[Dict[str, Any]]:
        """Get latest authentication information"""
        try:
            auth_info = self.db.query(AuthInfo).order_by(AuthInfo.created_at.desc()).first()
            if auth_info:
                return {
                    "id": auth_info.id,
                    "app_key": auth_info.app_key,
                    "app_secret": auth_info.app_secret,
                    "access_token": auth_info.access_token,
                    "token_type": auth_info.token_type,
                    "expires_in": auth_info.expires_in,
                    "created_at": auth_info.created_at.isoformat() if auth_info.created_at else None
                }
            return None
        except Exception as e:
            logger.error(f"Error getting auth info: {e}")
            raise
    
    async def save_auth_info(self, app_key: str, app_secret: str, 
                           access_token: str = None, token_type: str = None,
                           expires_in: int = None) -> Dict[str, Any]:
        """Save authentication information"""
        try:
            auth_info = AuthInfo(
                app_key=app_key,
                app_secret=app_secret,
                access_token=access_token,
                token_type=token_type,
                expires_in=expires_in
            )
            self.db.add(auth_info)
            self.db.commit()
            self.db.refresh(auth_info)
            
            return {
                "id": auth_info.id,
                "app_key": auth_info.app_key,
                "app_secret": auth_info.app_secret,
                "access_token": auth_info.access_token,
                "token_type": auth_info.token_type,
                "expires_in": auth_info.expires_in
            }
        except Exception as e:
            logger.error(f"Error saving auth info: {e}")
            self.db.rollback()
            raise
    
    async def authenticate_with_korea_investment(self, app_key: str, app_secret: str) -> Dict[str, Any]:
        """Authenticate with Korea Investment API"""
        try:
            # Korea Investment API authentication endpoint
            auth_url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "grant_type": "client_credentials",
                "appkey": app_key,
                "appsecret": app_secret
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(auth_url, headers=headers, json=data)
                response.raise_for_status()
                
                auth_response = response.json()
                
                # Save authentication info to database
                await self.save_auth_info(
                    app_key=app_key,
                    app_secret=app_secret,
                    access_token=auth_response.get("access_token"),
                    token_type=auth_response.get("token_type"),
                    expires_in=auth_response.get("expires_in")
                )
                
                return auth_response
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during authentication: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during Korea Investment authentication: {e}")
            raise
    
    async def is_token_valid(self) -> bool:
        """Check if current access token is valid"""
        try:
            auth_info = await self.get_auth_info()
            if not auth_info or not auth_info.get("access_token"):
                return False
            
            # Check if token is expired (assuming expires_in is in seconds)
            if auth_info.get("expires_in"):
                created_at = datetime.fromisoformat(auth_info["created_at"])
                expires_at = created_at + timedelta(seconds=auth_info["expires_in"])
                return datetime.now() < expires_at
            
            return True
        except Exception as e:
            logger.error(f"Error checking token validity: {e}")
            return False
