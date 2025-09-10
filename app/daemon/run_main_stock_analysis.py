"""
Run Main Stock Analysis

Converted from RunMainStockAnalysis.kt
Main analysis runner for stock trading decisions.
"""

import logging
from typing import Dict, Any
from app.services.krinvest.kr_inv_inq_service import KrInvInqService
from app.services.krinvest.kr_inv_ord_service import KrInvOrdService
from app.services.sa.sa_db_service import SaDbService
from app.services.sa.sa_stat_day_service import SaStatDayService
from app.services.sa.sa_stat_minute_service import SaStatMinuteService
from app.services.sa.sa_check_to_buy_service import SaCheckToBuyService
from app.services.sa.sa_check_to_sell_service import SaCheckToSellService
from app.services.sa.sa_common_service import SaCommonService

logger = logging.getLogger(__name__)

class RunMainStockAnalysis:
    """Main Stock Analysis Runner - converted from RunMainStockAnalysis.kt"""
    
    def __init__(
        self,
        kr_inv_inq_service: KrInvInqService,
        kr_inv_ord_service: KrInvOrdService,
        sa_db_service: SaDbService,
        sa_stat_day_service: SaStatDayService,
        sa_stat_minute_service: SaStatMinuteService,
        sa_check_to_buy_service: SaCheckToBuyService,
        sa_check_to_sell_service: SaCheckToSellService,
        sa_common_service: SaCommonService
    ):
        self.kr_inv_inq_service = kr_inv_inq_service
        self.kr_inv_ord_service = kr_inv_ord_service
        self.sa_db_service = sa_db_service
        self.sa_stat_day_service = sa_stat_day_service
        self.sa_stat_minute_service = sa_stat_minute_service
        self.sa_check_to_buy_service = sa_check_to_buy_service
        self.sa_check_to_sell_service = sa_check_to_sell_service
        self.sa_common_service = sa_common_service
        logger.info("RunMainStockAnalysis Init...")
    
    async def run_check_to_buy_test(
        self, stock_code: str, stock_name: str, tr_date: str, tr_time: str
    ) -> Dict[str, Any]:
        """Run buy check test"""
        try:
            logger.info(f"Running buy check test for {stock_code} ({stock_name})")
            
            # Get current price
            price_info = await self.kr_inv_inq_service.api_inquire_price(stock_code)
            
            # Check buy conditions
            buy_condition = await self.sa_check_to_buy_service.check_buy_condition(
                stock_code, tr_date, tr_time
            )
            
            # Get statistics
            day_stats = await self.sa_stat_day_service.get_day_statistics(stock_code, tr_date)
            minute_stats = await self.sa_stat_minute_service.get_minute_statistics(
                stock_code, tr_date, tr_time
            )
            
            result = {
                "test_type": "BUY_TEST",
                "stock_code": stock_code,
                "stock_name": stock_name,
                "test_date": tr_date,
                "test_time": tr_time,
                "price_info": price_info,
                "buy_condition": buy_condition,
                "day_statistics": day_stats,
                "minute_statistics": minute_stats,
                "recommendation": "BUY" if buy_condition.get("buy_recommended", False) else "HOLD"
            }
            
            logger.info(f"Buy test completed for {stock_code}: {result['recommendation']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in buy check test for {stock_code}: {e}")
            raise
    
    async def run_check_to_sell_test(
        self, stock_code: str, stock_name: str, tr_date: str, tr_time: str
    ) -> Dict[str, Any]:
        """Run sell check test"""
        try:
            logger.info(f"Running sell check test for {stock_code} ({stock_name})")
            
            # Get current price
            price_info = await self.kr_inv_inq_service.api_inquire_price(stock_code)
            
            # Check sell conditions
            sell_condition = await self.sa_check_to_sell_service.check_sell_condition(
                stock_code, tr_date, tr_time
            )
            
            # Get statistics
            day_stats = await self.sa_stat_day_service.get_day_statistics(stock_code, tr_date)
            minute_stats = await self.sa_stat_minute_service.get_minute_statistics(
                stock_code, tr_date, tr_time
            )
            
            result = {
                "test_type": "SELL_TEST",
                "stock_code": stock_code,
                "stock_name": stock_name,
                "test_date": tr_date,
                "test_time": tr_time,
                "price_info": price_info,
                "sell_condition": sell_condition,
                "day_statistics": day_stats,
                "minute_statistics": minute_stats,
                "recommendation": "SELL" if sell_condition.get("sell_recommended", False) else "HOLD"
            }
            
            logger.info(f"Sell test completed for {stock_code}: {result['recommendation']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in sell check test for {stock_code}: {e}")
            raise
