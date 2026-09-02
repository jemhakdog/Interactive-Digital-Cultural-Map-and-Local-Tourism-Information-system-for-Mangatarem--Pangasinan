"""Vercel serverless entrypoint for the FastAPI backend.

Vercel's Python runtime looks for an ASGI app in this file. It re-exports the
real app from backend.app.main. Run locally with uvicorn, deploy with vercel.
"""
from backend.app.main import app  # noqa: F401