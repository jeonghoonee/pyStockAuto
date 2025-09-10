"""
Korea Investment Order Service

Converted from KrInvOrdService.kt
Handles stock order operations through Korea Investment API.
"""

import logging
from typing import Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from app.models import AuthInfo
from app.utils import WebClientUtil, JsonUtil
from app.common.kr_auth_info import KrAuthInfo

if TYPE_CHECKING:
    from app.services.krinvest.kr_inv_oauth_service import KrInvOauthService

logger = logging.getLogger(__name__)

class KrInvOrdService:
    """Korea Investment Order Service - converted from KrInvOrdService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        # Dynamic import to avoid circular dependency
        from app.services.krinvest.kr_inv_oauth_service import KrInvOauthService
        self.kr_inv_oauth_service = KrInvOauthService(db_session)
        logger.info("koreaInvestOrderService Init ........")
    
    async def order_cash_sell_by_market_price(
        self, auth_info_entity: AuthInfo, stock_code: str, stock_qty: str
    ) -> Dict[str, Any]:
        """
        Domestic stock order > Stock order (sell by market price)
        국내주식주문 > 주식 주문 (매도)
        """
        return await self._api_order_cash(
            auth_info_entity, "0801U", stock_code, stock_qty, "0", "01"
        )
    
    async def order_cash_buy_by_price(
        self, auth_info_entity: AuthInfo, stock_code: str, stock_qty: str, stock_price: str
    ) -> Dict[str, Any]:
        """
        Domestic stock order > Stock order (buy by specific price)
        국내주식주문 > 주식 주문 (매수)
        """
        return await self._api_order_cash(
            auth_info_entity, "0802U", stock_code, stock_qty, stock_price, "00"
        )
    
    async def order_cash_buy_by_market_price(
        self, auth_info_entity: AuthInfo, stock_code: str, stock_qty: str
    ) -> Dict[str, Any]:
        """
        Domestic stock order > Stock order (buy by market price)
        국내주식주문 > 주식 주문 (시장가 매수)
        """
        return await self._api_order_cash(
            auth_info_entity, "0802U", stock_code, stock_qty, "0", "01"
        )
    
    async def _api_order_cash(
        self,
        auth_info_entity: AuthInfo,
        order_id: str,
        stock_code: str,
        stock_qty: str,
        stock_price: str,
        ord_dvsn: str
    ) -> Dict[str, Any]:
        """
        Domestic stock order > Stock order (cash)
        국내주식주문 > 주식주문(현금)
        """
        uri = "/uapi/domestic-stock/v1/trading/order-cash"
        
        headers = {
            "content-type": "application/json; charset=UTF-8",
            "appkey": auth_info_entity.app_key,
            "appsecret": auth_info_entity.app_secret,
            "authorization": f"Bearer {await self.kr_inv_oauth_service.api_oauth2_token(auth_info_entity)}",
            "tr_id": f"{KrAuthInfo.get_tr_id(auth_info_entity)}{order_id}"
        }
        
        req_body = {
            "CANO": auth_info_entity.account_number[:8],
            "ACNT_PRDT_CD": auth_info_entity.account_number[8:],
            "PDNO": stock_code,
            "ORD_DVSN": ord_dvsn,  # 00:지정가, 01:시장가, 05:장전 시간외, 06:장후 시간외, 07:시간외 단일가
            "ORD_QTY": stock_qty,
            "ORD_UNPR": stock_price
        }
        
        base_url = KrAuthInfo.get_base_url(auth_info_entity)
        response = await WebClientUtil.post_request(
            f"{base_url}{uri}",
            data=req_body,
            headers=headers
        )
        
        return response
    
    async def order_cancel(
        self, auth_info_entity: AuthInfo, order_num: str
    ) -> str:
        """
        Domestic stock order > Order cancel
        국내주식주문 > 주식 정정 취소 주문
        """
        uri = "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        
        headers = {
            "content-type": "application/json; charset=UTF-8",
            "appkey": auth_info_entity.app_key,
            "appsecret": auth_info_entity.app_secret,
            "authorization": f"Bearer {await self.kr_inv_oauth_service.api_oauth2_token(auth_info_entity)}",
            "tr_id": f"{KrAuthInfo.get_tr_id(auth_info_entity)}0803U"  # 주식 정정 취소 주문
        }
        
        req_body = {
            "CANO": auth_info_entity.account_number[:8],
            "ACNT_PRDT_CD": "01",
            "KRX_FWDG_ORD_ORGNO": "",
            "ORGN_ODNO": order_num,  # 주문시 한국투자증권 시스템에서 채번된 주문번호
            "ORD_DVSN": "01",        # 00:지정가, 01:시장가, 05:장전 시간외, 06:장후 시간외, 07:시간외 단일가
            "RVSE_CNCL_DVSN_CD": "02",  # 정정: 01, 취소:02
            "ORD_QTY": "",           # 전량주문인 경우 입력 불필요
            "ORD_UNPR": "",          # 정정인 경우 정정 주문 1주당 가격
            "QTY_ALL_ORD_YN": "Y"    # "Y" 잔량 전부, "N" 잔량 일부
        }
        
        base_url = KrAuthInfo.get_base_url(auth_info_entity)
        response = await WebClientUtil.post_request(
            f"{base_url}{uri}",
            data=req_body,
            headers=headers
        )
        
        return str(response)
    
    async def api_inquire_balance(self, auth_info_entity: AuthInfo) -> Dict[str, Any]:
        """
        Domestic stock order > Stock balance inquiry
        국내주식주문 > 주식 잔고 조회
        """
        uri = "/uapi/domestic-stock/v1/trading/inquire-balance"
        
        params = {
            "CANO": auth_info_entity.account_number[:8],
            "ACNT_PRDT_CD": "01",
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",      # 01: 대출일 별, 02: 종목 별
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",      # 00: 전일매매포함, 01: 전일매매 미포함
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        
        headers = {
            "content-type": "application/json; charset=utf-8",
            "appkey": auth_info_entity.app_key,
            "appsecret": auth_info_entity.app_secret,
            "authorization": f"Bearer {await self.kr_inv_oauth_service.api_oauth2_token(auth_info_entity)}",
            "tr_id": f"{KrAuthInfo.get_tr_id(auth_info_entity)}8434R"
        }
        
        base_url = KrAuthInfo.get_base_url(auth_info_entity)
        response = await WebClientUtil.get_request(
            f"{base_url}{uri}",
            headers=headers,
            params=params
        )
        
        return response
    
    async def api_inquire_ccnl(
        self, auth_info_entity: AuthInfo, order_date: str = None
    ) -> Dict[str, Any]:
        """
        Domestic stock order > Order execution inquiry
        국내주식주문 > 주문체결조회
        """
        uri = "/uapi/domestic-stock/v1/trading/inquire-ccnl"
        
        if order_date is None:
            from app.utils import DateUtil
            order_date = DateUtil.get_current_date_string()
        
        params = {
            "CANO": auth_info_entity.account_number[:8],
            "ACNT_PRDT_CD": auth_info_entity.account_number[8:],
            "INQR_STRT_DT": order_date,
            "INQR_END_DT": order_date,
            "SLL_BUY_DVSN_CD": "00",  # 00: 전체, 01: 매도, 02: 매수
            "INQR_DVSN": "00",
            "PDNO": "",
            "CCLD_DVSN": "00",
            "ORD_GNO_BRNO": "",
            "ODNO": "",
            "INQR_DVSN_3": "00"
        }
        
        headers = {
            "content-type": "application/json; charset=utf-8",
            "appkey": auth_info_entity.app_key,
            "appsecret": auth_info_entity.app_secret,
            "authorization": f"Bearer {await self.kr_inv_oauth_service.api_oauth2_token(auth_info_entity)}",
            "tr_id": f"{KrAuthInfo.get_tr_id(auth_info_entity)}8001R"
        }
        
        base_url = KrAuthInfo.get_base_url(auth_info_entity)
        response = await WebClientUtil.get_request(
            f"{base_url}{uri}",
            headers=headers,
            params=params
        )
        
        return response
