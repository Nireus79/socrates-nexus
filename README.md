# Socrates Nexus

**Universal LLM client for production** - Works with Claude, GPT-4, Gemini, Llama, and any LLM.

Extracted from **18 months of production use** in [Socrates AI](https://github.com/Nireus79/Socrates) platform.

[![PyPI version](https://img.shields.io/pypi/v/socrates-nexus.svg)](https://pypi.org/project/socrates-nexus/)
[![Downloads](https://img.shields.io/pypi/dm/socrates-nexus.svg)](https://pypi.org/project/socrates-nexus/)
[![Tests](https://github.com/Nireus79/socrates-nexus/actions/workflows/test.yml/badge.svg)](https://github.com/Nireus79/socrates-nexus/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-73%25-brightgreen)](https://github.com/Nireus79/socrates-nexus/blob/main/tests)

## Why Socrates Nexus?

Most LLM clients handle the happy path. Socrates Nexus handles **production**:

- ✅ **Automatic retry logic** with exponential backoff (timeouts, rate limits, temporary errors)
- ✅ **Token usage tracking** - Know exactly what you're spending across providers
- ✅ **Streaming support** with helpers (not fighting with raw streams)
- ✅ **Async + sync APIs** - Choose what works for you
- ✅ **Multi-model fallback** - If Claude is down, try GPT-4
- ✅ **Type hints throughout** - Better IDE experience
- ✅ **Universal API** - Same code works with Claude, GPT-4, Gemini, Llama

## Quick Start

### Installation

```bash
# Install with Claude support
pip install socrates-nexus[anthropic]

# Or with all providers
pip install socrates-nexus[all]
```

### Basic Usage

```python
from socrates_nexus import LLMClient

# Create client for any LLM
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="your-api-key"
)

# Chat - automatic retries, token tracking included
response = client.chat("What is machine learning?")
print(response.content)
print(f"Cost: ${response.usage.cost_usd}")
```

### Multiple Providers (Same API)

```python
from socrates_nexus import LLMClient

# Claude
claude = LLMClient(provider="anthropic", model="claude-opus", api_key="sk-ant-...")

# GPT-4
gpt4 = LLMClient(provider="openai", model="gpt-4", api_key="sk-...")

# Gemini
gemini = LLMClient(provider="google", model="gemini-pro", api_key="...")

# Llama (local)
llama = LLMClient(provider="ollama", model="llama2", base_url="http://localhost:11434")

# All use the same API!
for client in [claude, gpt4, gemini, llama]:
    response = client.chat("Hello!")
    print(f"{client.config.provider}: {response.content}")
```

### Streaming

```python
client = LLMClient(provider="anthropic", model="claude-opus", api_key="...")

def on_chunk(chunk):
    print(chunk, end="", flush=True)

response = client.stream("Write a poem about AI", on_chunk=on_chunk)
print(f"\n\nTotal cost: ${response.usage.cost_usd}")
```

### Async

```python
import asyncio
from socrates_nexus import AsyncLLMClient

async def main():
    client = AsyncLLMClient(
        provider="anthropic",
        model="claude-opus",
        api_key="..."
    )

    # Concurrent requests
    responses = await asyncio.gather(
        client.chat("Query 1"),
        client.chat("Query 2"),
        client.chat("Query 3"),
    )

    for response in responses:
        print(response.content)

asyncio.run(main())
```

## Configuration

### Common Configuration Options

```python
from socrates_nexus import LLMClient, LLMConfig

config = LLMConfig(
    # Provider and model
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",

    # Retry behavior
    retry_attempts=3,
    retry_backoff_factor=2.0,
    request_timeout=60,

    # Response caching
    cache_responses=True,
    cache_ttl=300,  # 5 minutes

    # Optional
    temperature=0.7,
    max_tokens=1024,
)

client = LLMClient(config=config)
```

### Environment Variables

Socrates Nexus automatically reads these if config not provided:
- `ANTHROPIC_API_KEY` - Anthropic Claude
- `OPENAI_API_KEY` - OpenAI GPT
- `GOOGLE_API_KEY` - Google Gemini
- `ANTHROPIC_BASE_URL` - Custom Anthropic endpoint
- `OPENAI_BASE_URL` - Custom OpenAI endpoint

## Error Handling

Socrates Nexus provides specific exception types for programmatic error handling:

```python
from socrates_nexus import (
    NexusError,
    RateLimitError,
    AuthenticationError,
    InvalidAPIKeyError,
    TimeoutError,
    ContextLengthExceededError,
    ModelNotFoundError,
)

try:
    response = client.chat("Query")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except ContextLengthExceededError as e:
    print(f"Input too long: {e.message}")
except NexusError as e:
    print(f"LLM Error ({e.error_code}): {e.message}")
```

All exceptions include:
- `message` - Human-readable error description
- `error_code` - Machine-readable error code
- `context` - Dict with provider-specific details

## Key Features

### 1. **Automatic Retries**

Handles transient failures automatically:
- Rate limits (HTTP 429)
- Timeout errors
- Temporary server errors (5xx)
- Exponential backoff with jitter

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="...",
    retry_attempts=3,           # Number of retries
    retry_backoff_factor=2.0,   # Exponential backoff multiplier
)
```

### 2. **Token Tracking**

Track usage and costs across all providers:

```python
response = client.chat("Query")

print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total cost: ${response.usage.cost_usd}")

# Get cumulative stats
stats = client.get_usage_stats()
print(f"Total spent: ${stats.total_cost_usd}")
```

### 3. **Multi-LLM Fallback & Resilience**

Build resilient applications with multiple fallback strategies:

**Sequential Fallback** - Try providers in order:
```python
def safe_chat(message: str):
    providers = [
        {"provider": "anthropic", "model": "claude-opus", "api_key": "..."},
        {"provider": "openai", "model": "gpt-4", "api_key": "..."},
        {"provider": "google", "model": "gemini-pro", "api_key": "..."},
    ]

    for config in providers:
        try:
            client = LLMClient(**config)
            return client.chat(message)
        except Exception:
            continue
    raise Exception("All providers failed")
```

**Parallel Fallback** - Try all at once, use first successful:
```python
import asyncio
from socrates_nexus import AsyncLLMClient

async def parallel_fallback(message: str):
    clients = [
        AsyncLLMClient(provider="anthropic", model="claude-opus", api_key="..."),
        AsyncLLMClient(provider="openai", model="gpt-4", api_key="..."),
    ]

    results = await asyncio.gather(
        *[c.chat(message) for c in clients],
        return_exceptions=True
    )

    for result in results:
        if not isinstance(result, Exception):
            return result
```

### 4. **Token Usage Tracking**

Real-time cost tracking with provider breakdowns:

```python
client = LLMClient(provider="anthropic", model="claude-opus", api_key="...")

# Track per-request
response = client.chat("What is Python?")
print(f"This request cost: ${response.usage.cost_usd:.6f}")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")

# Track cumulative usage
stats = client.get_usage_stats()
print(f"Total spent across all requests: ${stats.total_cost_usd:.2f}")
print(f"Total requests: {stats.total_requests}")

# Per-provider breakdown
for provider, p_stats in stats.by_provider.items():
    print(f"{provider}: {p_stats['requests']} requests, ${p_stats['cost_usd']:.2f}")

# Custom tracking callbacks
def log_expensive_requests(usage):
    if usage.cost_usd > 0.01:
        print(f"Expensive request: ${usage.cost_usd:.6f}")

client.add_usage_callback(log_expensive_requests)
```

### 5. **Response Caching**

Cache identical requests to save cost and time:

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="...",
    cache_responses=True,
    cache_ttl=300,  # 5 minutes
)

# First call: hits API
response1 = client.chat("What is Python?")

# Second call within 5 min: uses cache (instant)
response2 = client.chat("What is Python?")

print(f"Saved: ${response1.usage.cost_usd * 0.9}")
```

## Supported Providers

| Provider | Models | API Key | Status |
|----------|--------|---------|--------|
| **Anthropic** | Claude 3 (Opus, Sonnet, Haiku), Claude 3.5 Sonnet | Required | ✅ Full |
| **OpenAI** | GPT-4, GPT-4o, GPT-3.5-turbo | Required | ✅ Full |
| **Google** | Gemini 1.5 Pro, Gemini 1.5 Flash | Required | ✅ Full |
| **Ollama** | Llama 2, Mistral, Neural Chat, Orca (local) | Not required | ✅ Full |

### Setup Each Provider

**Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**OpenAI GPT:**
```bash
export OPENAI_API_KEY="sk-..."
```

**Google Gemini:**
```bash
export GOOGLE_API_KEY="..."
```

**Ollama (Local):**
```bash
# Install Ollama: https://ollama.ai
ollama pull llama2
ollama serve  # Starts on http://localhost:11434
# No API key needed!
```

## Examples

See the `examples/` directory for complete, runnable examples:

- **`01_anthropic_basic.py`** - Basic Claude usage, token tracking, and cost calculation
- **`02_openai_gpt4.py`** - OpenAI GPT-4 usage with streaming
- **`03_google_gemini.py`** - Google Gemini basic and streaming calls
- **`04_ollama_local.py`** - Local LLM with Ollama (no API key required)
- **`05_streaming.py`** - Streaming patterns: real-time output, chunk accumulation, progress tracking
- **`06_async_calls.py`** - Async/await, concurrent requests, multi-provider parallel execution
- **`07_token_tracking.py`** - Usage statistics, cost monitoring, per-provider breakdowns
- **`08_error_handling.py`** - Error types, safe error catching, automatic retry behavior
- **`09_provider_fallback.py`** - Provider fallback strategies: sequential, parallel, cost-optimized, model escalation

## Documentation

- [Quick Start](docs/quickstart.md) - Get started in 5 minutes
- [Providers Guide](docs/providers.md) - Setup for each LLM provider
- [API Reference](docs/api-reference.md) - Complete API documentation
- [Advanced Usage](docs/advanced.md) - Caching, fallbacks, monitoring
- [Architecture](docs/architecture.md) - System design and patterns
- [Comparison](docs/comparison.md) - vs LangChain, LiteLLM, and others
- [Roadmap](ROADMAP.md) - Feature roadmap and milestones

## Development

### Setup

```bash
# Clone repo
git clone https://github.com/Nireus79/socrates-nexus.git
cd socrates-nexus

# Install dev dependencies
pip install -e ".[dev,all]"

# Run tests
pytest tests/ -v

# Format code
black src/ tests/
ruff check src/ tests/
```

### Testing

```bash
# All tests
pytest tests/ -v

# Only fast tests
pytest tests/ -v -m "not slow"

# With coverage
pytest tests/ --cov=socrates_nexus --cov-report=html
```

## Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE)

## Origins

Socrates Nexus is extracted from [Socrates AI](https://github.com/Nireus79/Socrates), a collaborative AI platform. It's battle-tested in production and used for orchestrating multiple LLMs.

## Roadmap

### Phase 1: Foundation (Days 1-14) ✅ Complete
- ✅ Base client structure (sync + async)
- ✅ Provider implementations (Claude, GPT-4, Gemini, Ollama)
- ✅ Streaming support for all providers
- ✅ Automatic retry logic with exponential backoff
- ✅ Token tracking and cost calculation
- ✅ Response caching (TTL-based)
- ✅ Multi-provider fallback patterns
- ✅ 9 comprehensive examples
- ✅ Error handling with specific exception types

### Phase 2: Enhancement (Days 15-21) 🔄 In Progress
- 🔄 Unit tests (75%+ coverage target)
- 🔄 Integration tests
- ⏳ Vision models support
- ⏳ Function calling for all providers
- ⏳ Batch processing API

### Phase 3: Production (Days 22+) ⏳ Planned
- ⏳ Monitoring and observability
- ⏳ Rate limit optimization
- ⏳ Extended model support (Cohere, Replicate, etc.)
- ⏳ GitHub Actions CI/CD
- ⏳ PyPI publishing

## Support

- **Issues**: [GitHub Issues](https://github.com/Nireus79/socrates-nexus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nireus79/socrates-nexus/discussions)
- **Sponsor**: [GitHub Sponsors](https://github.com/sponsors/Nireus79)

---

**Made with ❤️ as part of the Socrates ecosystem**
