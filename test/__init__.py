"""
This module initializes the TestClient for the FastAPI application.

The client is configured to interact with the endpoints defined in the
`api.book_endpoints` module. This setup is useful for running tests and
interacting with the application programmatically.

Contents:
- TestClient instance for the FastAPI app from `api.book_endpoints`
"""

from fastapi.testclient import TestClient

from api.book_endpoints import app

client = TestClient(app)
