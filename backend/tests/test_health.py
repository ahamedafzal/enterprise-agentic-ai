def test_placeholder():
    """Placeholder test — real tests added from Day 3 onwards."""
    assert True


def test_app_imports():
    """Verify core modules import without errors."""
    from backend.core.config import settings
    assert settings.APP_NAME == "NEXUS - Enterprise Agentic AI"
    assert settings.APP_VERSION == "1.0.0"