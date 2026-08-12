import os
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_health(client, monkeypatch):
    monkeypatch.setattr("app.client", type("MockClient", (), {
        "admin": type("MockAdmin", (), {
            "command": lambda self, *a, **kw: True
        })()
    })())
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
