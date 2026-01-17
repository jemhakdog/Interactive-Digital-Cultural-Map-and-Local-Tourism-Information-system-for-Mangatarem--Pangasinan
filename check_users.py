import os

# Suppress prints from app.py by mocking some things or just ignoring them
from app import app
from models import User, db

with app.app_context():
    users = User.query.all()
    print("START_USERS")
    for user in users:
        print(f"USER|{user.username}|{user.role}|{user.is_approved}")
    print("END_USERS")
