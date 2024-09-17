#!/usr/bin/env python3
"""Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required"""
        return False

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request"""
        return request
