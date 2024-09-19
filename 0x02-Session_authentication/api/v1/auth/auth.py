#!/usr/bin/env python3
"""Authentication module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required"""
        if path is None or excluded_paths is None:
            return True
        for p in excluded_paths:
            if p[-1] == '*' and path.startswith(p[:-1]):
                return False
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_id = getenv('SESSION_NAME', None)
        return request.cookies.get(session_id)
