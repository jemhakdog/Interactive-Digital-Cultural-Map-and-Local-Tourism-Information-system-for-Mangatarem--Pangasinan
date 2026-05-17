"""
Verify Vercel performance quick wins are correctly applied.

Tests: Cache-Control headers, lazy Supabase loading, no auto-migrations on cold start.
"""
import os

# Simulate Vercel before importing app
os.environ["VERCEL"] = "1"
os.environ["DB_PROVIDER"] = "sqlite"

# Remove VERCEL to let sqlite work (we just test the IS_VERCEL flag was read)
# Actually, we can't use sqlite with VERCEL. Let's use a different approach.
del os.environ["VERCEL"]


def test_app_imports_without_error():
    """App should import without errors."""
    from app import app
    assert app is not None


def test_cache_control_absent_locally():
    """Cache-Control should NOT be set when IS_VERCEL is False."""
    from app import app
    with app.test_client() as c:
        r = c.get("/")
        assert r.status_code == 200
        assert "s-maxage" not in (r.headers.get("Cache-Control") or "")


def test_lazy_supabase_descriptor_exists():
    """Supabase should be accessible via app.supabase (lazy descriptor)."""
    from app import app
    supabase_descriptor = app.__class__.__dict__.get("supabase")
    assert supabase_descriptor is not None
    assert hasattr(supabase_descriptor, "__get__")
    assert supabase_descriptor.__class__.__name__ == "LazySupabase"


def test_record_view_no_commit():
    """record_view should run in a background thread to avoid blocking."""
    import inspect
    from modules.analytics.utils import record_view
    source = inspect.getsource(record_view)
    assert "threading.Thread" in source


def test_pooler_bug_fixed():
    """db_manager should check supabase.co, not supabase.com."""
    import inspect
    from utils.db_manager import _get_supabase_uri
    source = inspect.getsource(_get_supabase_uri)
    assert '"supabase.co"' in source
    assert '"supabase.com"' not in source


def test_no_auto_migration_on_vercel():
    """_run_auto_migrations should NOT be called at module level for Vercel."""
    import inspect
    import app as app_module
    # Check that _run_auto_migrations is NOT called in the module-level with block
    source = inspect.getsource(app_module)
    # The old code had "_run_auto_migrations()" - it should now be commented out or removed
    assert "_run_auto_migrations()" not in source.split("# Auto-migrations removed")[0].split("with app.app_context():")[-1]
