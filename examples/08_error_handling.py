"""
Example 8: Error Handling and Retry Logic

Demonstrates error handling and automatic retry behavior.
"""

import os
from socrates_nexus import (
    LLMClient,
    LLMError,
    RateLimitError,
    InvalidAPIKeyError,
    AuthenticationError,
    ContextLengthExceededError,
)

print("=" * 60)
print("ERROR HANDLING - INVALID API KEY")
print("=" * 60)

# Example 1: Invalid API key
print("\nAttempting to use invalid API key...\n")

try:
    client = LLMClient(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key="invalid-key-123",
    )

    response = client.chat("Hello")

except AuthenticationError as e:
    print(f"Authentication Error: {e.message}")
    print(f"Error Code: {e.error_code}")

except LLMError as e:
    print(f"LLM Error: {e.message}")

# Example 2: Invalid provider
print("\n" + "=" * 60)
print("ERROR HANDLING - INVALID PROVIDER")
print("=" * 60)

print("\nAttempting to use invalid provider...\n")

try:
    client = LLMClient(
        provider="invalid-provider",
        model="some-model",
        api_key="some-key",
    )

    response = client.chat("Hello")

except Exception as e:
    print(f"Error: {e}")

# Example 3: Handling various error types
print("\n" + "=" * 60)
print("ERROR HANDLING - COMPREHENSIVE ERROR CATCHING")
print("=" * 60)


def safe_chat(provider, model, api_key, message):
    """Safely make a chat request with error handling."""
    try:
        client = LLMClient(
            provider=provider,
            model=model,
            api_key=api_key,
        )

        response = client.chat(message)
        print(f"Success: {response.content[:100]}...")
        return response

    except RateLimitError as e:
        print(f"Rate Limit: {e.message}")
        if e.retry_after:
            print(f"  Retry after {e.retry_after} seconds")

    except InvalidAPIKeyError as e:
        print(f"Invalid API Key: {e.message}")

    except AuthenticationError as e:
        print(f"Authentication Failed: {e.message}")

    except ContextLengthExceededError as e:
        print(f"Context Too Long: {e.message}")

    except LLMError as e:
        print(f"LLM Error ({e.error_code}): {e.message}")

    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {e}")


print("\nTest 1: Invalid API key")
safe_chat("anthropic", "claude-haiku-4-5-20251001", "invalid-key", "Hello")

print("\nTest 2: Invalid provider")
safe_chat("invalid-provider", "some-model", "some-key", "Hello")

# Example 4: Retry logic (automatic, built-in)
print("\n" + "=" * 60)
print("ERROR HANDLING - AUTOMATIC RETRY LOGIC")
print("=" * 60)

print("\nNote: Retry logic is automatic and built-in!")
print("- Rate limits (429): retries with exponential backoff")
print("- Timeouts: retries up to max_attempts times")
print("- Server errors (5xx): retries with backoff and jitter")
print("\nConfiguration via LLMConfig:")
print("  - retry_attempts: default 3")
print("  - retry_backoff_factor: default 2.0 (exponential multiplier)")

client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

print("\nSending request (will auto-retry if it fails)...\n")

try:
    response = client.chat("This request will succeed if API is available")
    print(f"Success! Cost: ${response.usage.cost_usd:.6f}")

except LLMError as e:
    print(f"Failed after retries: {e.message}")
