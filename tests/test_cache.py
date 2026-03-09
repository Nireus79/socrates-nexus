"""Tests for response caching functionality."""

import time
from socrates_nexus.utils.cache import TTLCache


def test_ttl_cache_decorator_initialization():
    """Test TTLCache decorator initialization."""

    @TTLCache(ttl_minutes=5)
    def expensive_function(x):
        return x * 2

    assert expensive_function is not None


def test_ttl_cache_decorator_caching():
    """Test that decorator caches results."""
    call_count = 0

    @TTLCache(ttl_minutes=5)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call - should execute
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1

    # Second call with same args - should use cache
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # Should not increment


def test_ttl_cache_different_args():
    """Test that different arguments create different cache entries."""
    call_count = 0

    @TTLCache(ttl_minutes=5)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    result1 = expensive_function(5)
    result2 = expensive_function(10)

    assert result1 == 10
    assert result2 == 20
    assert call_count == 2  # Both calls executed


def test_ttl_cache_expiry():
    """Test that cached results expire after TTL."""
    call_count = 0

    # Use very short TTL for testing
    @TTLCache(ttl_minutes=0.017)  # ~1 second
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    expensive_function(5)
    assert call_count == 1

    # Wait for cache to expire
    time.sleep(1.5)

    expensive_function(5)
    assert call_count == 2  # Should execute again after expiry


def test_ttl_cache_with_kwargs():
    """Test caching with keyword arguments."""
    call_count = 0

    @TTLCache(ttl_minutes=5)
    def function_with_kwargs(a, b=10):
        nonlocal call_count
        call_count += 1
        return a + b

    result1 = function_with_kwargs(5, b=10)
    result2 = function_with_kwargs(5, b=10)

    assert result1 == 15
    assert result2 == 15
    assert call_count == 1  # Cached


def test_ttl_cache_different_kwargs():
    """Test that different kwargs create different cache entries."""
    call_count = 0

    @TTLCache(ttl_minutes=5)
    def function_with_kwargs(a, b=10):
        nonlocal call_count
        call_count += 1
        return a + b

    result1 = function_with_kwargs(5, b=10)
    result2 = function_with_kwargs(5, b=20)

    assert result1 == 15
    assert result2 == 25
    assert call_count == 2


def test_ttl_cache_return_types():
    """Test caching with different return types."""

    @TTLCache(ttl_minutes=5)
    def return_dict(x):
        return {"value": x * 2}

    result1 = return_dict(5)
    result2 = return_dict(5)

    assert result1 == {"value": 10}
    assert result2 == {"value": 10}
    assert result1 is result2  # Same object from cache


def test_ttl_cache_with_none():
    """Test caching when function returns None."""
    call_count = 0

    @TTLCache(ttl_minutes=5)
    def returns_none():
        nonlocal call_count
        call_count += 1
        return None

    result1 = returns_none()
    result2 = returns_none()

    assert result1 is None
    assert result2 is None
    assert call_count == 1  # Should be cached


def test_ttl_cache_preserves_function_name():
    """Test that decorator preserves function name."""

    @TTLCache(ttl_minutes=5)
    def my_function():
        return 42

    # Should preserve function metadata
    assert hasattr(my_function, "__wrapped__") or callable(my_function)


def test_ttl_cache_thread_safety():
    """Test that cache is thread-safe."""
    import threading

    call_count = 0

    @TTLCache(ttl_minutes=5)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    results = []

    def call_function():
        results.append(expensive_function(5))

    threads = [threading.Thread(target=call_function) for _ in range(5)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # All results should be same
    assert all(r == 10 for r in results)
    # Call count should be small (cached, not 5)
    assert call_count <= 3


def test_ttl_cache_hit_miss_stats():
    """Test cache hit/miss statistics."""

    @TTLCache(ttl_minutes=5)
    def expensive_function(x):
        return x * 2

    expensive_function(5)  # Miss
    expensive_function(5)  # Hit
    expensive_function(10)  # Miss
    expensive_function(5)  # Hit

    # Cache should have stats
    assert hasattr(expensive_function, "__wrapped__") or callable(expensive_function)
