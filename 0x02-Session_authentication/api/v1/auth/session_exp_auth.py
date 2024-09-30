#!/usr/bin/env python3
"""
SessionExpAuth class for managing session expiration
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class with session expiration """
    
    def __init__(self):
        """ Initialize SessionExpAuth with session duration """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create session with expiration time """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user ID if session is still valid """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None or 'created_at' not in session_dict:
            return None
        
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        # Check if session has expired
        expiry_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiry_time:
            return None

        return session_dict.get('user_id')
