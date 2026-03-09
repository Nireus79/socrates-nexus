# Quick Start Guide

Get started with Socrates Nexus in 5 minutes.

## 1. Installation

```bash
# Install with your preferred provider
pip install socrates-nexus[anthropic]      # For Claude
pip install socrates-nexus[openai]         # For GPT-4
pip install socrates-nexus[google]         # For Gemini
pip install socrates-nexus[ollama]         # For local models

# Or install with all providers
pip install socrates-nexus[all]
```

## 2. Set Up API Keys

### Anthropic Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"
```
Get your key: https://console.anthropic.com

### OpenAI GPT
```bash
export OPENAI_API_KEY="sk-YOUR-KEY-HERE"
```
Get your key: https://platform.openai.com/api-keys

### Google Gemini
```bash
export GOOGLE_API_KEY="YOUR-KEY-HERE"
```
Get your key: https://makersuite.google.com/app/apikey

### Ollama (Local, No Key Needed)
```bash
# Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai

# Pull a model
ollama pull llama2

# Start Ollama server
ollama serve
```

## 3. Your First Request

### Sync Version
```python
from socrates_nexus import LLMClient

client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key="sk-ant-...",  # or use env var
)

response = client.chat("What is machine learning?")
print(response.content)
print(f"Cost: ${response.usage.cost_usd:.6f}")
```

### Async Version
```python
import asyncio
from socrates_nexus import AsyncLLMClient

async def main():
    client = AsyncLLMClient(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key="sk-ant-...",
    )

    response = await client.chat("What is machine learning?")
    print(response.content)

asyncio.run(main())
```

## 4. Try Different Providers

Using the same API for all providers:

```python
from socrates_nexus import LLMClient

providers = [
    LLMClient(provider="anthropic", model="claude-opus", api_key="..."),
    LLMClient(provider="openai", model="gpt-4", api_key="..."),
    LLMClient(provider="google", model="gemini-pro", api_key="..."),
    LLMClient(provider="ollama", model="llama2"),  # No key needed
]

for client in providers:
    response = client.chat("Hello!")
    print(f"{client.config.provider}: {response.content[:50]}...")
```

## 5. Streaming Responses

Print as they arrive:

```python
client = LLMClient(provider="anthropic", model="claude-opus", api_key="...")

def print_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Write a short poem about AI",
    on_chunk=print_chunk,
)

print(f"\n\nTotal cost: ${response.usage.cost_usd:.6f}")
```

## 6. Tracking Costs

Monitor your spending across requests:

```python
client = LLMClient(provider="anthropic", model="claude-opus", api_key="...")

# Per-request tracking
response = client.chat("Query 1")
print(f"Request 1 cost: ${response.usage.cost_usd:.6f}")

response = client.chat("Query 2")
print(f"Request 2 cost: ${response.usage.cost_usd:.6f}")

# Cumulative stats
stats = client.get_usage_stats()
print(f"Total spent: ${stats.total_cost_usd:.6f}")
print(f"Total requests: {stats.total_requests}")
```

## 7. Handle Errors

Retry with different models on failure:

```python
from socrates_nexus import LLMClient, NexusError, RateLimitError

def chat_with_fallback(message: str):
    providers = [
        {"provider": "anthropic", "model": "claude-opus", "api_key": "..."},
        {"provider": "openai", "model": "gpt-4", "api_key": "..."},
    ]

    for config in providers:
        try:
            client = LLMClient(**config)
            return client.chat(message)
        except RateLimitError as e:
            print(f"Rate limited on {config['provider']}")
            continue
        except NexusError as e:
            print(f"Error: {e.message}")
            continue

    raise Exception("All providers failed")

response = chat_with_fallback("What is Python?")
print(response.content)
```

## 8. Async Parallel Requests

Send multiple requests concurrently:

```python
import asyncio
from socrates_nexus import AsyncLLMClient

async def main():
    client = AsyncLLMClient(
        provider="anthropic",
        model="claude-opus",
        api_key="...",
    )

    # Run 3 requests in parallel
    responses = await asyncio.gather(
        client.chat("What is Python?"),
        client.chat("What is JavaScript?"),
        client.chat("What is Rust?"),
    )

    for i, response in enumerate(responses, 1):
        print(f"{i}. {response.content[:50]}...")

asyncio.run(main())
```

## 9. Configuration Options

```python
from socrates_nexus import LLMClient, LLMConfig

config = LLMConfig(
    # Provider
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",

    # Generation options
    temperature=0.7,        # 0.0-1.0, lower = more deterministic
    max_tokens=1024,        # Max response length

    # Retry behavior
    retry_attempts=3,                   # Number of retries on failure
    retry_backoff_factor=2.0,          # Exponential backoff multiplier
    request_timeout=60,                # Timeout in seconds

    # Caching
    cache_responses=True,              # Cache identical requests
    cache_ttl=300,                     # Cache duration in seconds
)

client = LLMClient(config=config)
```

## 10. Next Steps

- Check out the [examples/](../examples/) directory for complete examples
- Read the [API Reference](api-reference.md) for detailed documentation
- See [Providers Guide](providers.md) for provider-specific setup
- Learn [Advanced Usage](advanced.md) for caching, callbacks, and monitoring

## Troubleshooting

### "No API key provided"
```bash
# Make sure your API key is set
export ANTHROPIC_API_KEY="sk-ant-..."

# Or pass it directly
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",
)
```

### "Connection refused" (Ollama)
```bash
# Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434
```

### "Rate limit exceeded"
Socrates Nexus automatically retries with exponential backoff. To customize:

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="...",
    retry_attempts=5,               # More retries
    retry_backoff_factor=3.0,      # Longer delays
)
```

### "Context length exceeded"
The model's context window is too small for your request. Try:
- A more powerful model
- Shorter input
- Streaming for large outputs

```python
# Upgrade to larger context model
client = LLMClient(
    provider="anthropic",
    model="claude-opus",  # Larger context than Haiku
    api_key="...",
)
```

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Nireus79/socrates-nexus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nireus79/socrates-nexus/discussions)
- **Documentation**: [Docs](../docs/)
