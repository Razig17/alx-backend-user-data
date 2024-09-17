#!/usr/bin/env python3
"""Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required"""
        if path is None or excluded_paths is None:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request"""
        return request
