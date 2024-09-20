#!/usr/bin/env python3
"""Session expiration module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration Class"""
    def __init__(self):
        """Initialize a session that can expire"""
        super().__init__()
        duration = getenv('SESSION_DURATION', '0')
        self.session_duration = 0
        if duration.isdigit():
            self.session_duration = int(duration)

    def create_session(self, user_id=None):
        """Creates a session id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary['user_id']
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary['created_at']
        span = timedelta(seconds=self.session_duration)
        if created_at + span < datetime.now():
            return None
        return session_dictionary['user_id']
