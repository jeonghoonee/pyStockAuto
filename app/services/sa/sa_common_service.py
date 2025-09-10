"""
SA Common Service

Converted from SaCommonService.kt
Common utilities and functions for Stock Analysis.
"""

import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.services.sa.sa_db_service import SaDbService
from app.utils import DateUtil, CommUtil

logger = logging.getLogger(__name__)

class SaCommonService:
    """SA Common Service - converted from SaCommonService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.sa_db_service = SaDbService(db_session)
        logger.info("SaCommonService Init...")
    
    async def get_stock_status(self, stock_code: str) -> Dict[str, Any]:
        """Get current stock status"""
        try:
            return {
                "stock_code": stock_code,
                "status": "ACTIVE",
                "last_update": DateUtil.get_current_datetime_string()
            }
        except Exception as e:
            logger.error(f"Error getting stock status for {stock_code}: {e}")
            raise
    
    def calculate_percentage_change(self, current_price: float, previous_price: float) -> float:
        """Calculate percentage change"""
        if previous_price == 0:
            return 0.0
        return ((current_price - previous_price) / previous_price) * 100
    
    def format_price(self, price: float) -> str:
        """Format price with proper decimal places"""
        return f"{price:,.2f}"
    
    def is_trading_hours(self) -> bool:
        """Check if current time is within trading hours"""
        # TODO: Implement proper trading hours check
        return True
