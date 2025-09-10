"""
Test Utilities

Tests for utility functions.
"""

import pytest
from datetime import datetime
from app.utils import DateUtil, JsonUtil, CommUtil

class TestDateUtil:
    """Test DateUtil functions"""
    
    def test_get_current_date_string(self):
        """Test get current date string"""
        date_str = DateUtil.get_current_date_string()
        assert len(date_str) == 8  # YYYYMMDD format
        assert date_str.isdigit()
    
    def test_get_current_time_string(self):
        """Test get current time string"""
        time_str = DateUtil.get_current_time_string()
        assert len(time_str) == 6  # HHMMSS format
        assert time_str.isdigit()
    
    def test_parse_date_string(self):
        """Test parse date string"""
        date_str = "20231201"
        parsed_date = DateUtil.parse_date_string(date_str)
        assert isinstance(parsed_date, datetime)
        assert parsed_date.year == 2023
        assert parsed_date.month == 12
        assert parsed_date.day == 1

class TestJsonUtil:
    """Test JsonUtil functions"""
    
    def test_to_json(self):
        """Test object to JSON conversion"""
        test_obj = {"name": "test", "value": 123}
        json_str = JsonUtil.to_json(test_obj)
        assert isinstance(json_str, str)
        assert "test" in json_str
        assert "123" in json_str
    
    def test_from_json(self):
        """Test JSON to object conversion"""
        json_str = '{"name": "test", "value": 123}'
        obj = JsonUtil.from_json(json_str)
        assert isinstance(obj, dict)
        assert obj["name"] == "test"
        assert obj["value"] == 123
    
    def test_is_valid_json(self):
        """Test JSON validation"""
        valid_json = '{"name": "test"}'
        invalid_json = '{"name": "test"'
        
        assert JsonUtil.is_valid_json(valid_json) == True
        assert JsonUtil.is_valid_json(invalid_json) == False

class TestCommUtil:
    """Test CommUtil functions"""
    
    def test_is_empty(self):
        """Test empty value checking"""
        assert CommUtil.is_empty(None) == True
        assert CommUtil.is_empty("") == True
        assert CommUtil.is_empty("   ") == True
        assert CommUtil.is_empty([]) == True
        assert CommUtil.is_empty({}) == True
        assert CommUtil.is_empty("test") == False
        assert CommUtil.is_empty([1, 2, 3]) == False
    
    def test_safe_get(self):
        """Test safe dictionary access"""
        test_dict = {"key1": "value1", "key2": "value2"}
        
        assert CommUtil.safe_get(test_dict, "key1") == "value1"
        assert CommUtil.safe_get(test_dict, "key3") is None
        assert CommUtil.safe_get(test_dict, "key3", "default") == "default"
    
    def test_generate_request_id(self):
        """Test request ID generation"""
        request_id = CommUtil.generate_request_id()
        assert isinstance(request_id, str)
        assert len(request_id) > 0
        
        # Generate another ID and ensure they're different
        another_id = CommUtil.generate_request_id()
        assert request_id != another_id
