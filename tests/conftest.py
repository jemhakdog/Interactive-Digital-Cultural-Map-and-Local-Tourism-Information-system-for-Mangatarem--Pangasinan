"""
Pytest configuration and fixtures for SQL injection tests.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    
    # Create database tables for testing
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up after tests
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """A database session for testing."""
    with app.app_context():
        yield db.session
