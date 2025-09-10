"""
Utility Functions

Common utility functions converted from Kotlin util classes.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import httpx
import asyncio

logger = logging.getLogger(__name__)

class DateUtil:
    """Date utility functions - converted from DateUtil.kt"""
    
    @staticmethod
    def get_current_date_string(format_str: str = "%Y%m%d") -> str:
        """Get current date as string"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def get_current_time_string(format_str: str = "%H%M%S") -> str:
        """Get current time as string"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def get_current_datetime_string(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get current datetime as string"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def parse_date_string(date_str: str, format_str: str = "%Y%m%d") -> datetime:
        """Parse date string to datetime object"""
        return datetime.strptime(date_str, format_str)
    
    @staticmethod
    def add_days(base_date: datetime, days: int) -> datetime:
        """Add days to a date"""
        return base_date + timedelta(days=days)

class JsonUtil:
    """JSON utility functions - converted from JacksonUtil.kt"""
    
    @staticmethod
    def to_json(obj: Any) -> str:
        """Convert object to JSON string"""
        try:
            return json.dumps(obj, default=str, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error converting to JSON: {e}")
            raise
    
    @staticmethod
    def from_json(json_str: str) -> Dict[str, Any]:
        """Parse JSON string to dictionary"""
        try:
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            raise
    
    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """Check if string is valid JSON"""
        try:
            json.loads(json_str)
            return True
        except:
            return False

class WebClientUtil:
    """Web client utility functions - converted from WebClientUtil.kt"""
    
    @staticmethod
    async def get_request(url: str, headers: Optional[Dict[str, str]] = None,
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error making GET request to {url}: {e}")
            raise
    
    @staticmethod
    async def post_request(url: str, data: Optional[Dict[str, Any]] = None,
                          headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make POST request"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error making POST request to {url}: {e}")
            raise

class CommUtil:
    """Common utility functions - converted from CommUtil.kt"""
    
    @staticmethod
    def is_empty(value: Any) -> bool:
        """Check if value is empty"""
        if value is None:
            return True
        if isinstance(value, str):
            return len(value.strip()) == 0
        if isinstance(value, (list, dict, tuple)):
            return len(value) == 0
        return False
    
    @staticmethod
    def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Safely get value from dictionary"""
        return dictionary.get(key, default)
    
    @staticmethod
    def generate_request_id() -> str:
        """Generate unique request ID"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def format_number(number: float, decimal_places: int = 2) -> str:
        """Format number with specified decimal places"""
        return f"{number:.{decimal_places}f}"

class FileUtil:
    """File utility functions - converted from FileUtil.kt"""
    
    @staticmethod
    async def read_file_async(file_path: str) -> str:
        """Read file asynchronously"""
        try:
            import aiofiles
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                return await file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    @staticmethod
    async def write_file_async(file_path: str, content: str) -> None:
        """Write file asynchronously"""
        try:
            import aiofiles
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
                await file.write(content)
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            raise
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file synchronously"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """Write file synchronously"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            raise
