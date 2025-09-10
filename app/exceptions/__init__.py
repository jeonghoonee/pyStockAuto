"""
Custom Exceptions

Custom exception classes for PyStockAuto application.
Converted from Kotlin exception classes.
"""

class PyStockAutoException(Exception):
    """Base exception for PyStockAuto application"""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class BizRuntimeException(PyStockAutoException):
    """Business logic runtime exception - converted from BizRuntimeException.kt"""
    
    def __init__(self, message: str, error_code: str = "BIZ_ERROR"):
        super().__init__(message, error_code)

class AuthenticationException(PyStockAutoException):
    """Authentication related exception"""
    
    def __init__(self, message: str = "Authentication failed", error_code: str = "AUTH_ERROR"):
        super().__init__(message, error_code)

class OrderException(PyStockAutoException):
    """Order related exception"""
    
    def __init__(self, message: str, error_code: str = "ORDER_ERROR"):
        super().__init__(message, error_code)

class DatabaseException(PyStockAutoException):
    """Database related exception"""
    
    def __init__(self, message: str, error_code: str = "DB_ERROR"):
        super().__init__(message, error_code)

class ExternalAPIException(PyStockAutoException):
    """External API related exception"""
    
    def __init__(self, message: str, error_code: str = "API_ERROR", status_code: int = None):
        self.status_code = status_code
        super().__init__(message, error_code)

class ValidationException(PyStockAutoException):
    """Data validation exception"""
    
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR", field: str = None):
        self.field = field
        super().__init__(message, error_code)
