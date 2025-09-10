"""
Result Codes

Converted from ResultCode.kt
Defines result codes and HTTP status mappings for API responses.
"""

from enum import Enum
from typing import Dict, Any

class ResultCode(Enum):
    """Result codes - converted from ResultCode.kt"""
    
    # Common result codes
    SUCCESS = (200, 200, "SUCCESS")
    FAIL = (200, 201, "FAIL")
    ERROR = (200, 202, "ERROR")
    DATA_NOT_FOUND = (200, 203, "There is no data")
    BAD_REQUEST = (400, 400, "This is invalid request.")
    INVALID_PARAMETER = (400, 401, "There are invalid parameters.")
    INVALID_USER_REQUEST_ENTITY = (400, 402, "There are Invalid Entity")
    ALREADY_RUNNING = (400, 403, "It is already running.")
    MALFORMED_REQUEST = (400, 409, "Your request payload is malformed")
    FORBIDDEN = (403, 403, "forbidden access")
    NOT_FOUND = (404, 404, "not found")
    UNEXPECTED_ERROR = (500, 500, "Internal Server ERROR")
    INVALID_TYPE_ERROR = (500, 501, "Invalid return type error")
    
    def __init__(self, http_status: int, code: int, default_message: str):
        self.http_status = http_status
        self.code = code
        self.default_message = default_message
    
    @classmethod
    def from_code(cls, code: int) -> "ResultCode":
        """Get ResultCode by code"""
        for result_code in cls:
            if result_code.code == code:
                return result_code
        raise ValueError(f"Unknown result code: {code}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "http_status": self.http_status,
            "code": self.code,
            "message": self.default_message
        }
