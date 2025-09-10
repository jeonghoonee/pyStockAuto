"""
Korea Investment Authentication Info Manager

Converted from KrAuthInfo.kt
Manages authentication information for Korea Investment API accounts.
"""

from typing import List, Optional
from app.models import AuthInfo
from app.constants.common_constant import CommonConstant

class KrAuthInfo:
    """Korea Investment Authentication Info Manager - converted from KrAuthInfo.kt"""
    
    _index = 0
    _index_real = 0
    _list_auth_info: List[AuthInfo] = []
    _list_real_auth_info: List[AuthInfo] = []
    
    @classmethod
    def set_auth_info_list(cls, auth_info_list: List[AuthInfo]):
        """Set authentication info lists"""
        print(f"Input listAuthInfo size : {len(auth_info_list)}")
        print(f"Input listRealAuthInfo size : {len(cls._list_real_auth_info)}")
        
        cls._list_auth_info.clear()
        cls._list_real_auth_info.clear()
        
        cls._list_auth_info.extend(auth_info_list)
        cls._list_real_auth_info.extend([auth for auth in auth_info_list if auth.mode == "R"])
        
        # Add first element again to handle concurrency issues (as in original Kotlin code)
        if cls._list_auth_info:
            cls._list_auth_info.append(auth_info_list[0])
        if cls._list_real_auth_info:
            cls._list_real_auth_info.append(cls._list_real_auth_info[0])
        
        print(f"listAuthInfo size : {len(cls._list_auth_info)}")
        print(f"listRealAuthInfo size : {len(cls._list_real_auth_info)}")
    
    @classmethod
    def get_tr_id(cls, auth_info_entity: AuthInfo) -> str:
        """Get transaction ID based on mode"""
        return "VTTC" if auth_info_entity.mode == "V" else "TTTC"
    
    @classmethod
    def get_base_url(cls, auth_info_entity: AuthInfo) -> str:
        """Get base URL based on mode"""
        return (CommonConstant.KR_INVEST_VIRTUAL_URL 
                if auth_info_entity.mode == "V" 
                else CommonConstant.KR_INVEST_REAL_URL)
    
    @classmethod
    def get_ws_url(cls, auth_info_entity: AuthInfo) -> str:
        """Get WebSocket URL based on mode"""
        return (CommonConstant.KR_INVEST_WS_VIRTUAL_URL 
                if auth_info_entity.mode == "V" 
                else CommonConstant.KR_INVEST_WS_REAL_URL)
    
    @classmethod
    def next(cls) -> AuthInfo:
        """Get next authentication info (round-robin)"""
        if not cls._list_auth_info:
            raise ValueError("No authentication info available")
        
        if cls._index >= len(cls._list_auth_info) - 1:
            cls._index = 0
        
        auth = cls._list_auth_info[cls._index]
        cls._index += 1
        
        return auth
    
    @classmethod
    def real_next(cls) -> AuthInfo:
        """Get next real mode authentication info (round-robin)"""
        if not cls._list_real_auth_info:
            raise ValueError("No real authentication info available")
        
        if cls._index_real >= len(cls._list_real_auth_info) - 1:
            cls._index_real = 0
        
        auth = cls._list_real_auth_info[cls._index_real]
        cls._index_real += 1
        
        return auth
    
    @classmethod
    @property
    def list_auth_info(cls) -> List[AuthInfo]:
        """Get all authentication info list"""
        return cls._list_auth_info
    
    @classmethod
    @property
    def list_real_auth_info(cls) -> List[AuthInfo]:
        """Get real mode authentication info list"""
        return cls._list_real_auth_info
