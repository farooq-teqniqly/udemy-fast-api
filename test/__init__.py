from fastapi.testclient import TestClient

from api.book_endpoints import app

client = TestClient(app)
