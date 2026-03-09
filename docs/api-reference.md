# API Reference

Complete API documentation for Socrates Nexus.

## Table of Contents

- [LLMClient](#llmclient)
- [AsyncLLMClient](#asyncllmclient)
- [Data Models](#data-models)
- [Exceptions](#exceptions)
- [Configuration](#configuration)

---

## LLMClient

Main synchronous client for interacting with LLM providers.

### Constructor

```python
from socrates_nexus import LLMClient, LLMConfig

client = LLMClient(
    provider="anthropic",           # "anthropic", "openai", "google", "ollama"
    model="claude-opus",            # Model name (required)
    api_key="sk-ant-...",          # API key (or use env var)
    temperature=0.7,               # 0.0-1.0, default 0.7
    max_tokens=1024,               # Max response length
    retry_attempts=3,              # Number of retries
    retry_backoff_factor=2.0,      # Exponential backoff multiplier
    request_timeout=60,            # Timeout in seconds
    cache_responses=False,         # Cache identical requests
    cache_ttl=300,                 # Cache duration in seconds
)

# Or use LLMConfig
config = LLMConfig(
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",
)
client = LLMClient(config=config)
```

### Methods

#### `chat(message: str, **kwargs) -> ChatResponse`

Send a single message and get a response.

```python
response = client.chat("What is machine learning?")

print(response.content)              # The response text
print(response.usage.total_tokens)   # Token usage
print(response.usage.cost_usd)       # Cost in USD
print(response.model)                # Model used
print(response.provider)             # Provider used
```

**Returns**: `ChatResponse` object with:
- `content: str` - The response text
- `usage: TokenUsage` - Token and cost information
- `model: str` - Model used
- `provider: str` - Provider used
- `raw_response: Any` - Raw provider response

#### `stream(message: str, on_chunk: Callable[[str], None], **kwargs) -> ChatResponse`

Stream a response with real-time chunk callbacks.

```python
def on_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Write a poem",
    on_chunk=on_chunk,
)

print(f"\n\nCost: ${response.usage.cost_usd}")
```

**Parameters**:
- `message: str` - Input message
- `on_chunk: Callable` - Function called for each chunk

**Returns**: `ChatResponse` object with accumulated response

#### `get_usage_stats() -> UsageStats`

Get cumulative usage statistics.

```python
stats = client.get_usage_stats()

print(f"Total requests: {stats.total_requests}")
print(f"Total tokens: {stats.total_tokens}")
print(f"Total cost: ${stats.total_cost_usd:.2f}")

# Per-provider breakdown
for provider, p_stats in stats.by_provider.items():
    print(f"{provider}: ${p_stats['cost_usd']:.2f}")

# Per-model breakdown
for model, m_stats in stats.by_model.items():
    print(f"{model}: {m_stats['requests']} requests")
```

**Returns**: `UsageStats` object with:
- `total_requests: int` - Total number of requests
- `total_input_tokens: int` - Total input tokens
- `total_output_tokens: int` - Total output tokens
- `total_tokens: int` - Total tokens (input + output)
- `total_cost_usd: float` - Total cost
- `by_provider: Dict` - Stats per provider
- `by_model: Dict` - Stats per model

#### `add_usage_callback(callback: Callable[[TokenUsage], None]) -> None`

Register a callback to be called after each request with token usage.

```python
def log_usage(usage: TokenUsage):
    print(f"Request cost: ${usage.cost_usd:.6f}")

client.add_usage_callback(log_usage)

# Now called after each chat/stream
response = client.chat("Query")
```

**Parameters**:
- `callback: Callable` - Function called with `TokenUsage` after each request

#### `clear_cache() -> None`

Clear the response cache (if enabled).

```python
client.clear_cache()
```

---

## AsyncLLMClient

Asynchronous version of LLMClient for async/await usage.

### Constructor

Same as `LLMClient`:

```python
from socrates_nexus import AsyncLLMClient

client = AsyncLLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",
)
```

### Methods

#### `async chat(message: str, **kwargs) -> ChatResponse`

Send a message asynchronously.

```python
import asyncio

async def main():
    response = await client.chat("What is Python?")
    print(response.content)

asyncio.run(main())
```

#### `async stream(message: str, on_chunk: Callable[[str], None], **kwargs) -> ChatResponse`

Stream a response asynchronously.

```python
async def main():
    def on_chunk(chunk: str):
        print(chunk, end="", flush=True)

    response = await client.stream(
        "Write a story",
        on_chunk=on_chunk,
    )
    print(f"\n\nCost: ${response.usage.cost_usd}")

asyncio.run(main())
```

#### `async gather_responses(messages: List[str]) -> List[ChatResponse]`

Send multiple messages concurrently using asyncio.gather.

```python
async def main():
    responses = await asyncio.gather(
        client.chat("Query 1"),
        client.chat("Query 2"),
        client.chat("Query 3"),
    )
    for response in responses:
        print(response.content)

asyncio.run(main())
```

#### `get_usage_stats() -> UsageStats`

Same as sync version.

#### `add_usage_callback(callback: Callable[[TokenUsage], None]) -> None`

Same as sync version.

---

## Data Models

### LLMConfig

Configuration for LLMClient.

```python
from socrates_nexus import LLMConfig

config = LLMConfig(
    provider="anthropic",           # str - required
    model="claude-opus",            # str - required
    api_key="sk-ant-...",          # str - optional (use env var)
    base_url="https://...",        # str - optional custom endpoint
    temperature=0.7,               # float - 0.0 to 1.0
    max_tokens=1024,               # int - max response length
    retry_attempts=3,              # int - number of retries
    retry_backoff_factor=2.0,      # float - exponential backoff
    request_timeout=60,            # int - timeout in seconds
    cache_responses=False,         # bool - cache identical requests
    cache_ttl=300,                 # int - cache duration in seconds
)
```

### ChatResponse

Response from a chat or stream request.

```python
response = client.chat("Hello")

# Attributes
response.content                # str - Response text
response.usage                  # TokenUsage - Token information
response.model                  # str - Model used
response.provider               # str - Provider used
response.raw_response          # Any - Raw provider response
response.timestamp             # datetime - When response was received
```

### TokenUsage

Token and cost information for a single request.

```python
usage = response.usage

# Attributes
usage.input_tokens             # int - Input tokens
usage.output_tokens            # int - Output tokens
usage.total_tokens             # int - Total (input + output)
usage.cost_usd                 # float - Cost in USD
usage.provider                 # str - Provider name
usage.model                    # str - Model name
usage.latency_ms               # float - Request latency in ms
usage.timestamp                # datetime - When request was made

# Calculated property
total_cost = usage.cost_usd    # Total cost for this request
```

### UsageStats

Cumulative usage statistics.

```python
stats = client.get_usage_stats()

# Attributes
stats.total_requests           # int - Total number of requests
stats.total_input_tokens       # int - Total input tokens
stats.total_output_tokens      # int - Total output tokens
stats.total_tokens             # int - Total tokens
stats.total_cost_usd           # float - Total cost
stats.by_provider              # Dict[str, Dict] - Per-provider stats
stats.by_model                 # Dict[str, Dict] - Per-model stats

# Example: Access per-provider stats
for provider, pstats in stats.by_provider.items():
    print(f"{provider}:")
    print(f"  Requests: {pstats['requests']}")
    print(f"  Tokens: {pstats['total_tokens']}")
    print(f"  Cost: ${pstats['cost_usd']:.2f}")
```

---

## Exceptions

All Socrates Nexus exceptions inherit from `NexusError`.

### NexusError

Base exception for all Socrates Nexus errors.

```python
from socrates_nexus import NexusError

try:
    response = client.chat("Query")
except NexusError as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
    print(f"Context: {e.context}")
```

**Attributes**:
- `message: str` - Human-readable error message
- `error_code: str` - Machine-readable error code
- `context: Dict` - Additional context (provider, model, etc.)

### RateLimitError

Rate limit exceeded. Includes retry information.

```python
from socrates_nexus import RateLimitError

try:
    response = client.chat("Query")
except RateLimitError as e:
    if e.retry_after:
        print(f"Retry after {e.retry_after} seconds")
    # Automatic retry happens - this is only if retries exhausted
```

**Additional Attributes**:
- `retry_after: Optional[int]` - Seconds to wait before retry

### AuthenticationError

Authentication failed (401/403).

```python
from socrates_nexus import AuthenticationError

try:
    response = client.chat("Query")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
```

### InvalidAPIKeyError

Invalid API key provided.

```python
from socrates_nexus import InvalidAPIKeyError

try:
    response = client.chat("Query")
except InvalidAPIKeyError as e:
    print(f"Invalid key: {e.message}")
```

### TimeoutError

Request timed out.

```python
from socrates_nexus import TimeoutError

try:
    response = client.chat("Query")
except TimeoutError as e:
    print(f"Request timed out after {e.context.get('timeout')} seconds")
```

### ContextLengthExceededError

Input exceeds model's context window.

```python
from socrates_nexus import ContextLengthExceededError

try:
    response = client.chat(very_long_message)
except ContextLengthExceededError as e:
    print(f"Context too long: {e.message}")
    # Try shorter input or more powerful model
```

### ModelNotFoundError

Model doesn't exist or isn't available.

```python
from socrates_nexus import ModelNotFoundError

try:
    response = client.chat("Query")
except ModelNotFoundError as e:
    print(f"Model not found: {e.message}")
```

### ProviderError

Provider-specific error.

```python
from socrates_nexus import ProviderError

try:
    response = client.chat("Query")
except ProviderError as e:
    print(f"Provider error: {e.message}")
```

### StreamingError

Error during streaming.

```python
from socrates_nexus import StreamingError

try:
    response = client.stream("Query", on_chunk=my_callback)
except StreamingError as e:
    print(f"Streaming failed: {e.message}")
```

### ConfigurationError

Invalid configuration.

```python
from socrates_nexus import ConfigurationError

try:
    client = LLMClient(provider="invalid", model="model")
except ConfigurationError as e:
    print(f"Config error: {e.message}")
```

### Example: Comprehensive Error Handling

```python
from socrates_nexus import (
    LLMClient,
    NexusError,
    RateLimitError,
    AuthenticationError,
    ContextLengthExceededError,
)

client = LLMClient(provider="anthropic", model="claude-opus", api_key="...")

try:
    response = client.chat("What is AI?")
    print(response.content)

except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    # Automatic retry already happened

except ContextLengthExceededError as e:
    print("Input too long, try shorter message or bigger model")

except AuthenticationError as e:
    print(f"Auth error: {e.message}")

except NexusError as e:
    print(f"General error ({e.error_code}): {e.message}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Configuration

### Environment Variables

Socrates Nexus automatically reads these if not provided:

```bash
# API Keys (provider-specific)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."

# Custom Endpoints (optional)
export ANTHROPIC_BASE_URL="https://..."
export OPENAI_BASE_URL="https://..."
export GOOGLE_BASE_URL="https://..."

# Defaults (optional)
export SOCRATES_NEXUS_PROVIDER="anthropic"
export SOCRATES_NEXUS_MODEL="claude-opus"
```

### Configuration Precedence

1. Explicit parameters to `LLMClient()`
2. Environment variables
3. Hard-coded defaults

```python
# This order:
client = LLMClient(
    provider="anthropic",    # 1. Use this
    # Falls back to ANTHROPIC_API_KEY env var
    # Falls back to default (error if none provided)
    api_key="sk-ant-...",
)
```

---

## Common Patterns

### Pattern 1: Multi-Provider Fallback

```python
def chat_with_fallback(message: str):
    providers = [
        {"provider": "anthropic", "model": "claude-opus", "api_key": "..."},
        {"provider": "openai", "model": "gpt-4", "api_key": "..."},
    ]

    for config in providers:
        try:
            client = LLMClient(**config)
            return client.chat(message)
        except Exception as e:
            print(f"{config['provider']} failed: {e}")
            continue

    raise Exception("All providers failed")
```

### Pattern 2: Parallel Requests

```python
import asyncio
from socrates_nexus import AsyncLLMClient

async def parallel_requests():
    client = AsyncLLMClient(provider="anthropic", model="claude-opus", api_key="...")

    responses = await asyncio.gather(
        client.chat("Query 1"),
        client.chat("Query 2"),
        client.chat("Query 3"),
    )

    return responses
```

### Pattern 3: Cost Monitoring

```python
# Track expensive requests
def log_expensive_requests(usage):
    if usage.cost_usd > 0.01:
        print(f"Expensive request! ${usage.cost_usd:.6f}")

client.add_usage_callback(log_expensive_requests)
```

### Pattern 4: Streaming with Progress

```python
import time

chunk_count = 0
start_time = time.time()

def progress_callback(chunk: str):
    global chunk_count
    chunk_count += 1
    elapsed = time.time() - start_time
    print(f"[{chunk_count} chunks, {elapsed:.1f}s] {chunk}", end="", flush=True)

response = client.stream("Query", on_chunk=progress_callback)
```

---

## Type Hints

All Socrates Nexus code includes type hints for better IDE support:

```python
from socrates_nexus import LLMClient, ChatResponse, TokenUsage
from typing import Optional

# Full type hints
response: ChatResponse = client.chat("Query")
usage: TokenUsage = response.usage
cost: float = usage.cost_usd

# Optional parameters
def process_response(response: Optional[ChatResponse]) -> None:
    if response:
        print(response.content)
```

---

## Performance

### Response Caching

Cache identical requests to improve speed and reduce costs:

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="...",
    cache_responses=True,
    cache_ttl=300,  # Cache for 5 minutes
)

# First call hits API
response1 = client.chat("What is Python?")

# Second call within 5 min uses cache (instant)
response2 = client.chat("What is Python?")
```

### Async Parallel Execution

Send multiple requests concurrently for better throughput:

```python
import asyncio

async def parallel_chat():
    client = AsyncLLMClient(...)

    # All 10 requests run in parallel
    responses = await asyncio.gather(*[
        client.chat(f"Query {i}")
        for i in range(10)
    ])

    return responses
```

---

## Next Steps

- [Quick Start](quickstart.md) - Get started in 5 minutes
- [Providers Guide](providers.md) - Setup instructions for each provider
- [Advanced Usage](advanced.md) - Caching, callbacks, and monitoring
- [Examples](../examples/) - Complete working examples
