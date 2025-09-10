"""
Database Models

This module contains all SQLAlchemy models converted from Kotlin entities.
"""

from sqlalchemy import Column, String, DateTime, Integer, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class StockCode(Base):
    """Stock Code Entity - converted from StockCodeEntity.kt"""
    __tablename__ = "stock_code"
    
    stock_code = Column(String(20), primary_key=True)
    stock_name = Column(String(100), nullable=False)
    date = Column(String(10), nullable=False)
    time = Column(String(8), nullable=False)
    
    def __repr__(self):
        return f"<StockCode(code={self.stock_code}, name={self.stock_name})>"

class StockList(Base):
    """Stock List Entity - converted from StockListEntity.kt"""
    __tablename__ = "stock_list"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    stock_name = Column(String(100), nullable=False)
    market = Column(String(10))
    sector = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AuthInfo(Base):
    """Auth Info Entity - converted from AuthInfoEntity.kt"""
    __tablename__ = "auth_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_key = Column(String(100), nullable=False)
    app_secret = Column(String(100), nullable=False)
    access_token = Column(Text)
    token_type = Column(String(20))
    expires_in = Column(Integer)
    access_token_expired_date = Column(String(50))
    approval_key = Column(String(200))
    account_number = Column(String(20))
    mode = Column(String(1))  # V for virtual, R for real
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AccountInfo(Base):
    """Account Info Entity - converted from AccountInfoEntity.kt"""
    __tablename__ = "account_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(String(20), nullable=False)
    account_name = Column(String(100))
    balance = Column(Float, default=0.0)
    available_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class OrderHistory(Base):
    """Order History Entity - converted from OrderHistoryEntity.kt"""
    __tablename__ = "order_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(50), unique=True, nullable=False)
    stock_code = Column(String(20), nullable=False)
    order_type = Column(String(10))  # BUY, SELL
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(20))  # PENDING, EXECUTED, CANCELLED
    order_time = Column(DateTime, default=func.now())
    execution_time = Column(DateTime)

class MonitoringList(Base):
    """Monitoring List Entity - converted from MonitoringListEntity.kt"""
    __tablename__ = "monitoring_list"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    target_price = Column(Float)
    stop_loss_price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class RunningThread(Base):
    """Running Thread Entity - converted from RunningThreadEntity.kt"""
    __tablename__ = "running_thread"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_name = Column(String(100), nullable=False)
    thread_type = Column(String(50))
    status = Column(String(20))  # RUNNING, STOPPED, ERROR
    start_time = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

class SearchLog(Base):
    """Search Log Entity - converted from SearchLogEntity.kt"""
    __tablename__ = "search_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_keyword = Column(String(200), nullable=False)
    search_type = Column(String(50))
    result_count = Column(Integer, default=0)
    search_time = Column(DateTime, default=func.now())

class MinuteData(Base):
    """Minute Data Entity - converted from MinuteDataEntity.kt"""
    __tablename__ = "minute_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    date_time = Column(DateTime, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer, default=0)

class AskingPrice(Base):
    """Asking Price Entity - converted from AskingPriceEntity.kt"""
    __tablename__ = "asking_price"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    bid_price_1 = Column(Float)
    bid_volume_1 = Column(Integer)
    ask_price_1 = Column(Float)
    ask_volume_1 = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

class DayStatEntity(Base):
    """Day Statistics Entity - converted from DayStatEntity.kt"""
    __tablename__ = "day_stat"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    tr_date = Column(String(10), nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

class MinuteStat(Base):
    """Minute Statistics Entity - converted from MinuteStatEntity.kt"""
    __tablename__ = "minute_stat"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False)
    tr_date = Column(String(10), nullable=False)
    tr_time = Column(String(6), nullable=False)
    stat_type = Column(String(20))
    stat_value = Column(Float)
    created_at = Column(DateTime, default=func.now())

class SearchResultLogEntity(Base):
    """Search Result Log Entity - converted from SearchResultLogEntity.kt"""
    __tablename__ = "search_result_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, nullable=False)
    result_data = Column(Text)
    result_type = Column(String(50))
    created_at = Column(DateTime, default=func.now())

class OrderCash(Base):
    """Order Cash Entity - converted from OrderCashEntity.kt"""
    __tablename__ = "order_cash"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(String(20), nullable=False)
    cash_balance = Column(Float, default=0.0)
    available_cash = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
