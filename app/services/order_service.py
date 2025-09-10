"""
Order Service

Business logic for order management and trading operations.
Converted from Kotlin order services.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models import OrderHistory, AccountInfo
from app.services.auth_service import AuthService
import logging
import httpx
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class OrderService:
    """Order-related business logic"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.auth_service = AuthService(db_session)
    
    async def place_buy_order(self, stock_code: str, quantity: int, price: float) -> Dict[str, Any]:
        """Place a buy order"""
        try:
            order_id = str(uuid.uuid4())
            
            # Create order record
            order = OrderHistory(
                order_id=order_id,
                stock_code=stock_code,
                order_type="BUY",
                quantity=quantity,
                price=price,
                status="PENDING"
            )
            
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            
            # TODO: Implement actual order placement with Korea Investment API
            # For now, just mark as executed for demonstration
            await self._execute_order(order)
            
            return {
                "order_id": order.order_id,
                "stock_code": order.stock_code,
                "order_type": order.order_type,
                "quantity": order.quantity,
                "price": order.price,
                "status": order.status
            }
        except Exception as e:
            logger.error(f"Error placing buy order: {e}")
            self.db.rollback()
            raise
    
    async def place_sell_order(self, stock_code: str, quantity: int, price: float) -> Dict[str, Any]:
        """Place a sell order"""
        try:
            order_id = str(uuid.uuid4())
            
            # Create order record
            order = OrderHistory(
                order_id=order_id,
                stock_code=stock_code,
                order_type="SELL",
                quantity=quantity,
                price=price,
                status="PENDING"
            )
            
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            
            # TODO: Implement actual order placement with Korea Investment API
            # For now, just mark as executed for demonstration
            await self._execute_order(order)
            
            return {
                "order_id": order.order_id,
                "stock_code": order.stock_code,
                "order_type": order.order_type,
                "quantity": order.quantity,
                "price": order.price,
                "status": order.status
            }
        except Exception as e:
            logger.error(f"Error placing sell order: {e}")
            self.db.rollback()
            raise
    
    async def get_order_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get order history"""
        try:
            orders = self.db.query(OrderHistory).order_by(
                OrderHistory.order_time.desc()
            ).limit(limit).all()
            
            return [
                {
                    "order_id": order.order_id,
                    "stock_code": order.stock_code,
                    "order_type": order.order_type,
                    "quantity": order.quantity,
                    "price": order.price,
                    "status": order.status,
                    "order_time": order.order_time.isoformat() if order.order_time else None,
                    "execution_time": order.execution_time.isoformat() if order.execution_time else None
                }
                for order in orders
            ]
        except Exception as e:
            logger.error(f"Error getting order history: {e}")
            raise
    
    async def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        try:
            order = self.db.query(OrderHistory).filter(
                OrderHistory.order_id == order_id
            ).first()
            
            if order:
                return {
                    "order_id": order.order_id,
                    "stock_code": order.stock_code,
                    "order_type": order.order_type,
                    "quantity": order.quantity,
                    "price": order.price,
                    "status": order.status,
                    "order_time": order.order_time.isoformat() if order.order_time else None,
                    "execution_time": order.execution_time.isoformat() if order.execution_time else None
                }
            return None
        except Exception as e:
            logger.error(f"Error getting order by ID {order_id}: {e}")
            raise
    
    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            order = self.db.query(OrderHistory).filter(
                OrderHistory.order_id == order_id
            ).first()
            
            if not order:
                raise ValueError(f"Order {order_id} not found")
            
            if order.status != "PENDING":
                raise ValueError(f"Cannot cancel order with status {order.status}")
            
            order.status = "CANCELLED"
            self.db.commit()
            
            return {
                "order_id": order.order_id,
                "status": order.status,
                "message": "Order cancelled successfully"
            }
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            self.db.rollback()
            raise
    
    async def _execute_order(self, order: OrderHistory) -> None:
        """Execute an order (simulate execution for now)"""
        try:
            # TODO: Implement actual order execution with broker API
            # For now, just mark as executed
            order.status = "EXECUTED"
            order.execution_time = datetime.now()
            self.db.commit()
            
            logger.info(f"Order {order.order_id} executed successfully")
        except Exception as e:
            logger.error(f"Error executing order {order.order_id}: {e}")
            order.status = "ERROR"
            self.db.commit()
            raise
    
    async def get_account_balance(self) -> Dict[str, Any]:
        """Get account balance information"""
        try:
            account = self.db.query(AccountInfo).first()
            if account:
                return {
                    "account_number": account.account_number,
                    "account_name": account.account_name,
                    "balance": account.balance,
                    "available_balance": account.available_balance,
                    "updated_at": account.updated_at.isoformat() if account.updated_at else None
                }
            return {
                "balance": 0.0,
                "available_balance": 0.0,
                "message": "No account information found"
            }
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            raise
