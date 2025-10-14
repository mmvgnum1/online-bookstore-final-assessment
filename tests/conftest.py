import pytest
import importlib
import app as app_module

@pytest.fixture(autouse=True)
def fresh_app_state(monkeypatch):
    """
    Ensure global cart/users/orders are reset between tests by reloading app module.
    """
    import sys
    if 'app' in sys.modules:
        importlib.reload(app_module)
    yield

@pytest.fixture()
def app():
    app_module.app.config.update(TESTING=True, SECRET_KEY="test")
    return app_module.app

@pytest.fixture()
def client(app):
    return app.test_client()
