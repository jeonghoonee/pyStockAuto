"""
SA Service

Converted from SaService.kt
Main service for Stock Analysis functionality.
"""

import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.services.krinvest.kr_inv_ord_service import KrInvOrdService
from app.services.krinvest.kr_inv_inq_service import KrInvInqService
from app.services.sa.sa_db_service import SaDbService
from app.services.sa.sa_stat_day_service import SaStatDayService
from app.services.sa.sa_stat_minute_service import SaStatMinuteService
from app.services.sa.sa_check_to_buy_service import SaCheckToBuyService
from app.services.sa.sa_check_to_sell_service import SaCheckToSellService
from app.services.sa.sa_common_service import SaCommonService
from app.daemon.run_main_stock_analysis import RunMainStockAnalysis
from app.utils import DateUtil, CommUtil

logger = logging.getLogger(__name__)

class SaService:
    """SA Service - converted from SaService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.kr_inv_ord_service = KrInvOrdService(db_session)
        self.kr_inv_inq_service = KrInvInqService(db_session)
        self.sa_db_service = SaDbService(db_session)
        self.sa_stat_day_service = SaStatDayService(db_session)
        self.sa_stat_minute_service = SaStatMinuteService(db_session)
        self.sa_check_to_buy_service = SaCheckToBuyService(db_session)
        self.sa_check_to_sell_service = SaCheckToSellService(db_session)
        self.sa_common_service = SaCommonService(db_session)
        logger.info("SaService Init...")
    
    async def run_buy_test(self, stock_code: str, tr_date: str, tr_time: str) -> Dict[str, Any]:
        """
        Run buy test for a specific stock
        특정 주식에 대한 매수 테스트 실행
        """
        try:
            # Get stock information
            stock = await self.sa_db_service.find_stock_by_stock_code(stock_code)
            if not stock:
                raise ValueError(f"Stock not found: {stock_code}")
            
            # Create analysis runner
            analysis_runner = RunMainStockAnalysis(
                kr_inv_inq_service=self.kr_inv_inq_service,
                kr_inv_ord_service=self.kr_inv_ord_service,
                sa_db_service=self.sa_db_service,
                sa_stat_day_service=self.sa_stat_day_service,
                sa_stat_minute_service=self.sa_stat_minute_service,
                sa_check_to_buy_service=self.sa_check_to_buy_service,
                sa_check_to_sell_service=self.sa_check_to_sell_service,
                sa_common_service=self.sa_common_service
            )
            
            # Run buy check test
            result = await analysis_runner.run_check_to_buy_test(
                stock_code=stock_code,
                stock_name=stock.stock_name,
                tr_date=tr_date,
                tr_time=tr_time
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error running buy test for {stock_code}: {e}")
            raise
    
    async def run_sell_test(self, stock_code: str, tr_date: str, tr_time: str) -> Dict[str, Any]:
        """
        Run sell test for a specific stock
        특정 주식에 대한 매도 테스트 실행
        """
        try:
            # Get stock information
            stock = await self.sa_db_service.find_stock_by_stock_code(stock_code)
            if not stock:
                raise ValueError(f"Stock not found: {stock_code}")
            
            # Create analysis runner
            analysis_runner = RunMainStockAnalysis(
                kr_inv_inq_service=self.kr_inv_inq_service,
                kr_inv_ord_service=self.kr_inv_ord_service,
                sa_db_service=self.sa_db_service,
                sa_stat_day_service=self.sa_stat_day_service,
                sa_stat_minute_service=self.sa_stat_minute_service,
                sa_check_to_buy_service=self.sa_check_to_buy_service,
                sa_check_to_sell_service=self.sa_check_to_sell_service,
                sa_common_service=self.sa_common_service
            )
            
            # Run sell check test
            result = await analysis_runner.run_check_to_sell_test(
                stock_code=stock_code,
                stock_name=stock.stock_name,
                tr_date=tr_date,
                tr_time=tr_time
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error running sell test for {stock_code}: {e}")
            raise
    
    async def analyze_stock_comprehensive(self, stock_code: str) -> Dict[str, Any]:
        """
        Perform comprehensive stock analysis
        종합적인 주식 분석 수행
        """
        try:
            current_date = DateUtil.get_current_date_string()
            current_time = DateUtil.get_current_time_string()
            
            # Get stock information
            stock = await self.sa_db_service.find_stock_by_stock_code(stock_code)
            if not stock:
                raise ValueError(f"Stock not found: {stock_code}")
            
            # Get current price
            price_info = await self.kr_inv_inq_service.api_inquire_price(stock_code)
            
            # Get daily statistics
            day_stats = await self.sa_stat_day_service.get_day_statistics(stock_code, current_date)
            
            # Get minute statistics
            minute_stats = await self.sa_stat_minute_service.get_minute_statistics(
                stock_code, current_date, current_time
            )
            
            # Check buy/sell signals
            buy_signal = await self.sa_check_to_buy_service.check_buy_condition(
                stock_code, current_date, current_time
            )
            
            sell_signal = await self.sa_check_to_sell_service.check_sell_condition(
                stock_code, current_date, current_time
            )
            
            return {
                "stock_code": stock_code,
                "stock_name": stock.stock_name,
                "analysis_date": current_date,
                "analysis_time": current_time,
                "price_info": price_info,
                "day_statistics": day_stats,
                "minute_statistics": minute_stats,
                "buy_signal": buy_signal,
                "sell_signal": sell_signal,
                "recommendation": self._get_recommendation(buy_signal, sell_signal)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock {stock_code}: {e}")
            raise
    
    def _get_recommendation(self, buy_signal: Dict[str, Any], sell_signal: Dict[str, Any]) -> str:
        """
        Get trading recommendation based on buy/sell signals
        매수/매도 신호를 기반으로 한 거래 추천
        """
        buy_score = buy_signal.get("score", 0)
        sell_score = sell_signal.get("score", 0)
        
        if buy_score > sell_score and buy_score > 0.7:
            return "BUY"
        elif sell_score > buy_score and sell_score > 0.7:
            return "SELL"
        else:
            return "HOLD"
