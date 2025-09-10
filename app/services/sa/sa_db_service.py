"""
SA Database Service

Converted from SaDbService.kt
Handles all database operations for Stock Analysis functionality.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app.models import (
    StockList, DayStatEntity, MinuteStat, MinuteData, AuthInfo,
    OrderHistory, MonitoringList, StockCode, SearchResultLogEntity,
    SearchLog, RunningThread, AskingPrice, OrderCash
)
from app.utils import DateUtil

logger = logging.getLogger(__name__)

class SaDbService:
    """SA Database Service - converted from SaDbService.kt"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        logger.info("StockAutoDbService Init ........")
    
    # stockListRepository methods
    async def save_all_stock_list(self, entity_list: List[StockList]) -> List[StockList]:
        """Save all stock list entities"""
        try:
            for entity in entity_list:
                self.db.add(entity)
            self.db.commit()
            return entity_list
        except Exception as e:
            logger.error(f"Error saving stock list: {e}")
            self.db.rollback()
            raise
    
    def find_all_stock_list(self) -> List[StockList]:
        """Find all stock list"""
        try:
            return self.db.query(StockList).all()
        except Exception as e:
            logger.error(f"Error finding all stock list: {e}")
            raise
    
    async def find_stock_by_stock_name(self, stock_name: str) -> Optional[StockList]:
        """Find stock by stock name"""
        try:
            return self.db.query(StockList).filter(StockList.stock_name == stock_name).first()
        except Exception as e:
            logger.error(f"Error finding stock by name {stock_name}: {e}")
            raise
    
    async def find_stock_by_stock_code(self, stock_code: str) -> Optional[StockList]:
        """Find stock by stock code"""
        try:
            return self.db.query(StockList).filter(StockList.stock_code == stock_code).first()
        except Exception as e:
            logger.error(f"Error finding stock by code {stock_code}: {e}")
            raise
    
    # dayInfoRepository methods
    async def save_day_info(self, entity: DayStatEntity) -> DayStatEntity:
        """Save day info entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving day info: {e}")
            self.db.rollback()
            raise
    
    async def find_day_info_by_stock_code_and_tr_date(self, stock_code: str, tr_date: str) -> Optional[DayStatEntity]:
        """Find day info by stock code and transaction date"""
        try:
            return self.db.query(DayStatEntity).filter(
                and_(DayStatEntity.stock_code == stock_code, DayStatEntity.tr_date == tr_date)
            ).first()
        except Exception as e:
            logger.error(f"Error finding day info for {stock_code} on {tr_date}: {e}")
            raise
    
    # minuteDataRepository methods
    async def save_all_minute_data_list(self, entity_list: List[MinuteData]) -> List[MinuteData]:
        """Save all minute data entities"""
        try:
            for entity in entity_list:
                self.db.add(entity)
            self.db.commit()
            return entity_list
        except Exception as e:
            logger.error(f"Error saving minute data list: {e}")
            self.db.rollback()
            raise
    
    async def find_minute_data_by_stock_code_and_tr_date_and_tr_time_period_desc(
        self, stock_code: str, tr_date: str, start_tr_time: str, end_tr_time: str
    ) -> List[MinuteData]:
        """Find minute data by time period in descending order"""
        try:
            return self.db.query(MinuteData).filter(
                and_(
                    MinuteData.stock_code == stock_code,
                    MinuteData.date_time >= f"{tr_date} {start_tr_time}",
                    MinuteData.date_time <= f"{tr_date} {end_tr_time}"
                )
            ).order_by(desc(MinuteData.date_time)).all()
        except Exception as e:
            logger.error(f"Error finding minute data by period: {e}")
            raise
    
    def find_minute_data_by_tr_time(self, stock_code: str, tr_date: str, tr_time: str) -> Optional[MinuteData]:
        """Find minute data by specific time"""
        try:
            return self.db.query(MinuteData).filter(
                and_(
                    MinuteData.stock_code == stock_code,
                    MinuteData.date_time == f"{tr_date} {tr_time}"
                )
            ).first()
        except Exception as e:
            logger.error(f"Error finding minute data by time: {e}")
            raise
    
    async def save_minute_data(self, entity: MinuteData) -> MinuteData:
        """Save minute data entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving minute data: {e}")
            self.db.rollback()
            raise
    
    # minuteStatRepository methods
    async def save_minute_stat(self, entity: MinuteStat) -> MinuteStat:
        """Save minute stat entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving minute stat: {e}")
            self.db.rollback()
            raise
    
    # authInfoRepository methods
    def find_all_auth_info_with_account(self) -> List[AuthInfo]:
        """Find all auth info with account"""
        try:
            return self.db.query(AuthInfo).filter(AuthInfo.account_number.isnot(None)).all()
        except Exception as e:
            logger.error(f"Error finding auth info with account: {e}")
            raise
    
    async def save_auth_info(self, entity: AuthInfo) -> AuthInfo:
        """Save auth info entity"""
        try:
            if entity.id:
                # Update existing
                self.db.merge(entity)
            else:
                # Create new
                self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving auth info: {e}")
            self.db.rollback()
            raise
    
    # orderHistoryRepository methods
    async def save_order_history(self, entity: OrderHistory) -> OrderHistory:
        """Save order history entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving order history: {e}")
            self.db.rollback()
            raise
    
    def find_order_history_by_stock_code_and_order_type(
        self, stock_code: str, order_type: str
    ) -> List[OrderHistory]:
        """Find order history by stock code and order type"""
        try:
            return self.db.query(OrderHistory).filter(
                and_(OrderHistory.stock_code == stock_code, OrderHistory.order_type == order_type)
            ).all()
        except Exception as e:
            logger.error(f"Error finding order history: {e}")
            raise
    
    # monitoringListRepository methods
    async def save_monitoring_list(self, entity: MonitoringList) -> MonitoringList:
        """Save monitoring list entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving monitoring list: {e}")
            self.db.rollback()
            raise
    
    def find_all_monitoring_list_active(self) -> List[MonitoringList]:
        """Find all active monitoring list"""
        try:
            return self.db.query(MonitoringList).filter(MonitoringList.is_active == True).all()
        except Exception as e:
            logger.error(f"Error finding active monitoring list: {e}")
            raise
    
    # stockCodeRepository methods
    async def save_stock_code(self, entity: StockCode) -> StockCode:
        """Save stock code entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving stock code: {e}")
            self.db.rollback()
            raise
    
    def find_all_stock_code(self) -> List[StockCode]:
        """Find all stock codes"""
        try:
            return self.db.query(StockCode).all()
        except Exception as e:
            logger.error(f"Error finding all stock codes: {e}")
            raise
    
    # runningThreadRepository methods
    async def save_running_thread(self, entity: RunningThread) -> RunningThread:
        """Save running thread entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving running thread: {e}")
            self.db.rollback()
            raise
    
    def find_running_thread_by_thread_name(self, thread_name: str) -> Optional[RunningThread]:
        """Find running thread by thread name"""
        try:
            return self.db.query(RunningThread).filter(RunningThread.thread_name == thread_name).first()
        except Exception as e:
            logger.error(f"Error finding running thread by name {thread_name}: {e}")
            raise
    
    # askingPriceRepository methods
    async def save_asking_price(self, entity: AskingPrice) -> AskingPrice:
        """Save asking price entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving asking price: {e}")
            self.db.rollback()
            raise
    
    # orderCachRepository methods
    async def save_order_cash(self, entity: OrderCash) -> OrderCash:
        """Save order cash entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            logger.error(f"Error saving order cash: {e}")
            self.db.rollback()
            raise
