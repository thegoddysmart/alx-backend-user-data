#!/usr/bin/env python3
""" SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for session management using database
    """

    def create_session(self, user_id=None):
        """ Creates and stores a session in the database """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Store the session in the database (file-based)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID by searching for the
        session ID in the database
        """
        if not session_id:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the session by removing it from the database
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
