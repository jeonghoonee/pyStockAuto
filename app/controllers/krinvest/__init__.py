"""
Korea Investment API Controllers

This module contains controllers for Korea Investment securities API integration.
Converted from the Kotlin krinvest package.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.krinvest.kr_inv_oauth_service import KrInvOauthService
from app.services.krinvest.kr_inv_ord_service import KrInvOrdService
from app.services.krinvest.kr_inv_inq_service import KrInvInqService
from app.services.sa.sa_api_service import SaApiService
from app.models import AuthInfo

router = APIRouter()

@router.get("/")
async def krinvest_root():
    """Root endpoint for Korea Investment API"""
    return {"message": "Korea Investment API endpoints"}

@router.get("/approval")
async def get_approval(db: Session = Depends(get_db)):
    """Get approval key for real-time websocket connection"""
    try:
        oauth_service = KrInvOauthService(db)
        approval_key = await oauth_service.api_oauth2_approval()
        return {"approval_key": approval_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tokenP")
async def get_token_p(auth_info: Dict[str, Any], db: Session = Depends(get_db)):
    """Get access token"""
    try:
        oauth_service = KrInvOauthService(db)
        # Convert dict to AuthInfo entity
        auth_entity = AuthInfo(**auth_info)
        access_token = await oauth_service.api_oauth2_token(auth_entity)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-cash-buy/{stock_code}/{stock_qty}/{stock_price}")
async def order_cash_buy_by_price(
    stock_code: str, stock_qty: str, stock_price: str, 
    db: Session = Depends(get_db)
):
    """Place a buy order with specific price"""
    try:
        api_service = SaApiService(db)
        result = await api_service.order_cash_buy_by_price(stock_code, stock_qty, stock_price)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-marketprice-buy/{stock_code}/{stock_qty}")
async def order_cash_buy_by_market_price(
    stock_code: str, stock_qty: str,
    db: Session = Depends(get_db)
):
    """Place a buy order at market price"""
    try:
        api_service = SaApiService(db)
        result = await api_service.order_cash_buy_by_market_price(stock_code, stock_qty)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-cash-sell/{stock_code}/{stock_qty}")
async def order_cash_sell_by_market_price(
    stock_code: str, stock_qty: str,
    db: Session = Depends(get_db)
):
    """Place a sell order at market price"""
    try:
        api_service = SaApiService(db)
        result = await api_service.order_cash_sell_by_market_price(stock_code, stock_qty)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-rvsecncl/{order_number}")
async def order_rvsecncl(order_number: str, db: Session = Depends(get_db)):
    """Cancel an order"""
    try:
        api_service = SaApiService(db)
        result = await api_service.order_rvsecncl(order_number)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inquire-price/{stock_code}")
async def inquire_price(stock_code: str, db: Session = Depends(get_db)):
    """Get current stock price"""
    try:
        inq_service = KrInvInqService(db)
        result = await inq_service.api_inquire_price(stock_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inquire-balance")
async def inquire_balance(account_number: str, db: Session = Depends(get_db)):
    """Get account balance"""
    try:
        inq_service = KrInvInqService(db)
        result = await inq_service.api_inquire_balance(account_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
