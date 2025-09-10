"""
Common Constants

Converted from CommonConstant.kt
Application-wide constants for PyStockAuto.
"""

class CommonConstant:
    """Common constants - converted from CommonConstant.kt"""
    
    DOMAIN = "biz.stock"
    X_REQUEST_ID_KEY = "X-Request-ID"
    AUTHORIZATION_KEY = "Authorization"
    BEARER_PREFIX = "Bearer "
    
    # Korea Investment API URLs
    KR_INVEST_REAL_URL = "https://openapi.koreainvestment.com:9443"
    KR_INVEST_VIRTUAL_URL = "https://openapivts.koreainvestment.com:29443"
    KR_INVEST_WS_REAL_URL = "ws://ops.koreainvestment.com:21000"
    KR_INVEST_WS_VIRTUAL_URL = "ws://ops.koreainvestment.com:31000"
    
    # Trading delays and repeats (in milliseconds converted to seconds)
    DELAY_BUY = 15.0  # 15000L milliseconds = 15 seconds
    DELAY_SELL = 3.0  # 3000L milliseconds = 3 seconds
    REPEAT_BUY = 360 * 6  # 2160
    REPEAT_SELL = REPEAT_BUY * 5  # 10800
