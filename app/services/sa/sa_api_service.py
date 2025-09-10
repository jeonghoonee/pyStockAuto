"""
SA API Service

Converted from SaApiService.kt
Main API service that orchestrates stock analysis and trading operations.
"""

import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.services.krinvest.kr_inv_ord_service import KrInvOrdService
from app.services.krinvest.kr_inv_inq_service import KrInvInqService
from app.services.sa.sa_db_service import SaDbService
from app.common.kr_auth_info import KrAuthInfo

logger = logging.getLogger(__name__)

class SaApiService:
    """SA API Service - converted from SaApiService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.kr_inv_ord_service = KrInvOrdService(db_session)
        self.kr_inv_inq_service = KrInvInqService(db_session)
        self.sa_db_service = SaDbService(db_session)
        logger.info("SaApiService Init...")
    
    async def order_cash_buy_by_price(
        self, stock_code: str, stock_qty: str, stock_price: str
    ) -> Dict[str, Any]:
        """Order cash buy by specific price"""
        try:
            auth_info = KrAuthInfo.next()
            result = await self.kr_inv_ord_service.order_cash_buy_by_price(
                auth_info, stock_code, stock_qty, stock_price
            )
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error in order_cash_buy_by_price: {e}")
            return {"status": "error", "message": str(e)}
    
    async def order_cash_buy_by_market_price(
        self, stock_code: str, stock_qty: str
    ) -> Dict[str, Any]:
        """Order cash buy by market price"""
        try:
            auth_info = KrAuthInfo.next()
            result = await self.kr_inv_ord_service.order_cash_buy_by_market_price(
                auth_info, stock_code, stock_qty
            )
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error in order_cash_buy_by_market_price: {e}")
            return {"status": "error", "message": str(e)}
    
    async def order_cash_sell_by_market_price(
        self, stock_code: str, stock_qty: str
    ) -> Dict[str, Any]:
        """Order cash sell by market price"""
        try:
            auth_info = KrAuthInfo.next()
            result = await self.kr_inv_ord_service.order_cash_sell_by_market_price(
                auth_info, stock_code, stock_qty
            )
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error in order_cash_sell_by_market_price: {e}")
            return {"status": "error", "message": str(e)}
    
    async def order_rvsecncl(self, order_number: str) -> str:
        """Cancel order"""
        try:
            auth_info = KrAuthInfo.next()
            result = await self.kr_inv_ord_service.order_cancel(auth_info, order_number)
            return result
        except Exception as e:
            logger.error(f"Error in order_rvsecncl: {e}")
            return f"Error: {str(e)}"
