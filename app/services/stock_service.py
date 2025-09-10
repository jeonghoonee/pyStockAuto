"""
Stock Service

Business logic for stock-related operations.
Converted from Kotlin stock services.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models import StockCode, StockList, MonitoringList
import logging

logger = logging.getLogger(__name__)

class StockService:
    """Stock-related business logic"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def get_all_stocks(self) -> List[Dict[str, Any]]:
        """Get all stocks from database"""
        try:
            stocks = self.db.query(StockCode).all()
            return [
                {
                    "stock_code": stock.stock_code,
                    "stock_name": stock.stock_name,
                    "date": stock.date,
                    "time": stock.time
                }
                for stock in stocks
            ]
        except Exception as e:
            logger.error(f"Error getting all stocks: {e}")
            raise
    
    async def get_stock_by_code(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """Get stock by code"""
        try:
            stock = self.db.query(StockCode).filter(StockCode.stock_code == stock_code).first()
            if stock:
                return {
                    "stock_code": stock.stock_code,
                    "stock_name": stock.stock_name,
                    "date": stock.date,
                    "time": stock.time
                }
            return None
        except Exception as e:
            logger.error(f"Error getting stock by code {stock_code}: {e}")
            raise
    
    async def search_stocks_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search stocks by name"""
        try:
            stocks = self.db.query(StockCode).filter(
                StockCode.stock_name.contains(name)
            ).all()
            return [
                {
                    "stock_code": stock.stock_code,
                    "stock_name": stock.stock_name,
                    "date": stock.date,
                    "time": stock.time
                }
                for stock in stocks
            ]
        except Exception as e:
            logger.error(f"Error searching stocks by name {name}: {e}")
            raise
    
    async def add_to_monitoring(self, stock_code: str, target_price: float = None, 
                               stop_loss_price: float = None) -> Dict[str, Any]:
        """Add stock to monitoring list"""
        try:
            monitoring_item = MonitoringList(
                stock_code=stock_code,
                target_price=target_price,
                stop_loss_price=stop_loss_price,
                is_active=True
            )
            self.db.add(monitoring_item)
            self.db.commit()
            self.db.refresh(monitoring_item)
            
            return {
                "id": monitoring_item.id,
                "stock_code": monitoring_item.stock_code,
                "target_price": monitoring_item.target_price,
                "stop_loss_price": monitoring_item.stop_loss_price,
                "is_active": monitoring_item.is_active
            }
        except Exception as e:
            logger.error(f"Error adding stock {stock_code} to monitoring: {e}")
            self.db.rollback()
            raise
    
    async def get_monitoring_list(self) -> List[Dict[str, Any]]:
        """Get all stocks in monitoring list"""
        try:
            monitoring_items = self.db.query(MonitoringList).filter(
                MonitoringList.is_active == True
            ).all()
            return [
                {
                    "id": item.id,
                    "stock_code": item.stock_code,
                    "target_price": item.target_price,
                    "stop_loss_price": item.stop_loss_price,
                    "created_at": item.created_at.isoformat() if item.created_at else None
                }
                for item in monitoring_items
            ]
        except Exception as e:
            logger.error(f"Error getting monitoring list: {e}")
            raise
