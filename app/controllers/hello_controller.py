"""
Hello Controller

Converted from HelloController.kt
Provides basic health check and greeting endpoints.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/hello")
async def get_hello():
    """
    Hello endpoint - converted from HelloController.kt
    Returns greeting message with current timestamp
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "message": f"Hello! PyStockAuto Start! ==> {formatted_time}",
        "timestamp": formatted_time,
        "service": "PyStockAuto"
    }
