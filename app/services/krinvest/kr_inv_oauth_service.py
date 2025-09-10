"""
Korea Investment OAuth Service

Converted from KrInvOauthService.kt
Handles authentication and token management for Korea Investment API.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import AuthInfo
from app.utils import DateUtil, WebClientUtil, JsonUtil
from app.common.kr_auth_info import KrAuthInfo
from app.services.sa.sa_db_service import SaDbService

logger = logging.getLogger(__name__)

class KrInvOauthService:
    """Korea Investment OAuth Service - converted from KrInvOauthService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.sa_db_service = SaDbService(db_session)
        logger.info("KoreaInvestOauthService Init ........")
        
        # Initialize auth info
        auth_info_list = self.sa_db_service.find_all_auth_info_with_account()
        KrAuthInfo.set_auth_info_list(auth_info_list)
        self._validate_auth_info(KrAuthInfo.list_auth_info)
    
    async def api_oauth2_approval(self, auth_info_entity: AuthInfo = None) -> str:
        """
        Real-time websocket access key issuance
        실시간 웹소켓 접속키 발급
        """
        if auth_info_entity is None:
            auth_info_entity = KrAuthInfo.next()
        
        current_time = DateUtil.get_current_datetime_string()
        
        if auth_info_entity.access_token_expired_date < current_time:
            logger.info(f"authInfoEntity approval : {auth_info_entity.account_number} {auth_info_entity.approval_key}")
            
            uri = "/oauth2/Approval"
            
            headers = {
                "content-type": "application/json"
            }
            
            req_body = {
                "grant_type": "client_credentials",
                "appkey": auth_info_entity.app_key,
                "secretkey": auth_info_entity.app_secret
            }
            
            base_url = KrAuthInfo.get_base_url(auth_info_entity)
            response = await WebClientUtil.post_request(
                f"{base_url}{uri}",
                data=req_body,
                headers=headers
            )
            
            logger.info(f"approval response: {response}")
            
            auth_info_entity.approval_key = response.get("approval_key", "")
            
            # Update entity
            updated_auth_info = await self.sa_db_service.save_auth_info(auth_info_entity)
            logger.info(f"authInfo approval : {updated_auth_info.account_number} {updated_auth_info.approval_key}")
        
        return auth_info_entity.approval_key
    
    async def api_oauth2_token(self, auth_info_entity: AuthInfo) -> str:
        """
        Access token issuance
        접근토큰 발급
        """
        current_time = DateUtil.get_current_datetime_string()
        
        if auth_info_entity.access_token_expired_date < current_time:
            logger.info(f"authInfoEntity token : {auth_info_entity.account_number} "
                       f"{auth_info_entity.access_token_expired_date} {auth_info_entity.access_token}")
            
            uri = "/oauth2/tokenP"
            
            headers = {
                "content-type": "application/json; charset=UTF-8"
            }
            
            req_body = {
                "grant_type": "client_credentials",
                "appkey": auth_info_entity.app_key,
                "appsecret": auth_info_entity.app_secret
            }
            
            base_url = KrAuthInfo.get_base_url(auth_info_entity)
            response = await WebClientUtil.post_request(
                f"{base_url}{uri}",
                data=req_body,
                headers=headers
            )
            
            auth_info_entity.access_token = response.get("access_token", "")
            auth_info_entity.access_token_expired_date = response.get("access_token_token_expired", "")
            
            # Update entity
            updated_auth_info = await self.sa_db_service.save_auth_info(auth_info_entity)
            logger.info(f"authInfo token : {updated_auth_info.account_number} "
                       f"{updated_auth_info.access_token_expired_date} {updated_auth_info.access_token}")
        
        return auth_info_entity.access_token
    
    async def api_revoke_token(self, auth_info_entity: AuthInfo) -> str:
        """
        Revoke access token
        접근토큰 폐기
        """
        uri = "/oauth2/revokeP"
        
        headers = {
            "content-type": "application/json; charset=UTF-8"
        }
        
        req_body = {
            "token": auth_info_entity.access_token,
            "appkey": auth_info_entity.app_key,
            "appsecret": auth_info_entity.app_secret
        }
        
        auth_info_entity.access_token = ""
        auth_info_entity.access_token_expired_date = ""
        
        await self.sa_db_service.save_auth_info(auth_info_entity)
        
        base_url = KrAuthInfo.get_base_url(auth_info_entity)
        response = await WebClientUtil.post_request(
            f"{base_url}{uri}",
            data=req_body,
            headers=headers
        )
        
        return response.get("msg1", "")
    
    async def _validate_auth_info(self, auth_info_list: List[AuthInfo]):
        """Validate authentication information for all accounts"""
        for auth_info in auth_info_list:
            await self.api_oauth2_token(auth_info)
            # await self.api_oauth2_approval(auth_info)
