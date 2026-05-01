# Session Management Helper
# This file provides session persistence handling for the Flask application

from flask import session


def make_session_permanent():
    """
    Make Flask sessions permanent to persist across browser restarts.
    Call this in a before_request handler.
    """
    session.permanent = True
