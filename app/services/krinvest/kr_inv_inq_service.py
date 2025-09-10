"""
Korea Investment Inquiry Service

Converted from KrInvInqService.kt
Handles stock inquiry operations through Korea Investment API.
"""

import logging
from typing import Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from app.models import AuthInfo, StockCode
from app.utils import WebClientUtil, JsonUtil
from app.common.kr_auth_info import KrAuthInfo

if TYPE_CHECKING:
    from app.services.krinvest.kr_inv_oauth_service import KrInvOauthService

logger = logging.getLogger(__name__)

class KrInvInqService:
    """Korea Investment Inquiry Service - converted from KrInvInqService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        # Dynamic import to avoid circular dependency
        from app.services.krinvest.kr_inv_oauth_service import KrInvOauthService
        self.kr_inv_oauth_service = KrInvOauthService(db_session)
        self.is_biz_day = False
        logger.info("KoreaInvestInquireService Init ........")
        self._set_biz_date_yn()
    
    async def api_inquire_price(self, stock_code: str, debug: bool = False) -> Dict[str, Any]:
        """
        Domestic stock quote > Current stock price quote
        국내주식시세 > 주식현재가 시세
        """
        auth_info_entity = KrAuthInfo.next()
        
        uri = "/uapi/domestic-stock/v1/quotations/inquire-price"
        url = f"{auth_info_entity.domain}{uri}"
        
        headers = self._get_default_headers(auth_info_entity, "FHKST01010100")
        
        parameters = {
            "FID_COND_MRKT_DIV_CODE": "J",  # J: Stock, ETF, ETN
            "FID_INPUT_ISCD": stock_code
        }
        
        try:
            response = await WebClientUtil.api_get_send(url, headers, parameters)
            
            if debug:
                logger.info(f"API Response: {response}")
            
            result = JsonUtil.get_json_object_as_dict(response)
            
            if self._is_success_response(result):
                return result
            else:
                logger.error(f"API Error: {result}")
                return {"error": "API request failed", "details": result}
                
        except Exception as e:
            logger.error(f"Exception in api_inquire_price: {e}")
            return {"error": str(e)}
    
    def _get_default_headers(self, auth_info: AuthInfo, tr_id: str) -> Dict[str, str]:
        """Get default headers for API requests"""
        return {
            "Content-Type": "application/json",
            "authorization": f"Bearer {auth_info.access_token}",
            "appkey": auth_info.app_key,
            "appsecret": auth_info.app_secret,
            "tr_id": tr_id,
            "custtype": "P"  # P: Personal, B: Business
        }
    
    def _is_success_response(self, response: Dict[str, Any]) -> bool:
        """Check if the API response indicates success"""
        return response.get("rt_cd") == "0"
    
    def _set_biz_date_yn(self):
        """Set business date flag"""
        # This would typically check if today is a business day
        # For now, we'll assume it's always a business day
        self.is_biz_day = True
        logger.info(f"Business day flag set to: {self.is_biz_day}")
