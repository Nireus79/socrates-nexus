# Providers Guide

Complete setup and usage instructions for each supported LLM provider.

## Table of Contents

- [Anthropic Claude](#anthropic-claude)
- [OpenAI GPT](#openai-gpt)
- [Google Gemini](#google-gemini)
- [Ollama (Local)](#ollama-local)
- [Provider Comparison](#provider-comparison)

---

## Anthropic Claude

### Setup

1. **Get API Key**
   - Go to https://console.anthropic.com
   - Sign up or log in
   - Create an API key in the "API Keys" section
   - Copy your key

2. **Set Environment Variable**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Or pass directly to client**
   ```python
   client = LLMClient(
       provider="anthropic",
       model="claude-opus",
       api_key="sk-ant-...",
   )
   ```

### Available Models

| Model | Context | Speed | Cost | Best For |
|-------|---------|-------|------|----------|
| `claude-opus` | 200K | Slowest | Highest | Complex reasoning |
| `claude-3-5-sonnet-20241022` | 200K | Balanced | Mid | General purpose |
| `claude-haiku-4-5-20251001` | 100K | Fastest | Lowest | Quick responses |

### Pricing (per million tokens)

- **Haiku**: $0.80 input / $4.00 output
- **Sonnet**: $3.00 input / $15.00 output
- **Opus**: $15.00 input / $75.00 output

### Example Usage

```python
from socrates_nexus import LLMClient

# Using default (Haiku - cheapest)
client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key="sk-ant-...",
)

response = client.chat("What is machine learning?")
print(f"Response: {response.content}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
```

### Streaming

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",
)

def on_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Write a poem about AI",
    on_chunk=on_chunk,
)
```

---

## OpenAI GPT

### Setup

1. **Get API Key**
   - Go to https://platform.openai.com/api-keys
   - Sign up or log in
   - Create a new API key
   - Copy your key

2. **Set Environment Variable**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. **Or pass directly to client**
   ```python
   client = LLMClient(
       provider="openai",
       model="gpt-4",
       api_key="sk-...",
   )
   ```

### Available Models

| Model | Context | Speed | Cost | Best For |
|-------|---------|-------|------|----------|
| `gpt-4` | 128K | Slowest | Highest | Complex reasoning |
| `gpt-4-turbo-preview` | 128K | Fast | Mid | Fast & capable |
| `gpt-3.5-turbo` | 128K | Fastest | Lowest | Quick responses |

### Pricing (per million tokens)

- **GPT-3.5-turbo**: $0.50 input / $1.50 output
- **GPT-4**: $30.00 input / $60.00 output
- **GPT-4-turbo**: $10.00 input / $30.00 output

### Example Usage

```python
from socrates_nexus import LLMClient

# Using GPT-3.5 (cheapest)
client = LLMClient(
    provider="openai",
    model="gpt-3.5-turbo",
    api_key="sk-...",
)

response = client.chat("Explain quantum computing")
print(f"Response: {response.content}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
```

### Streaming

```python
client = LLMClient(
    provider="openai",
    model="gpt-4",
    api_key="sk-...",
)

def on_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Write a short story",
    on_chunk=on_chunk,
)
```

### Custom Endpoint

For local OpenAI-compatible servers (LM Studio, Ollama, etc.):

```python
client = LLMClient(
    provider="openai",
    model="your-model-name",
    api_key="any-key",  # Can be dummy key
    base_url="http://localhost:8000",
)
```

---

## Google Gemini

### Setup

1. **Get API Key**
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API key"
   - Copy your key

2. **Set Environment Variable**
   ```bash
   export GOOGLE_API_KEY="..."
   ```

3. **Or pass directly to client**
   ```python
   client = LLMClient(
       provider="google",
       model="gemini-pro",
       api_key="...",
   )
   ```

### Available Models

| Model | Context | Speed | Cost | Best For |
|-------|---------|-------|------|----------|
| `gemini-1.5-pro` | 1M | Slowest | Higher | Long documents |
| `gemini-1.5-flash` | 1M | Fast | Lower | Quick responses |

### Pricing

Currently free tier available with rate limits.

### Example Usage

```python
from socrates_nexus import LLMClient

client = LLMClient(
    provider="google",
    model="gemini-1.5-flash",
    api_key="...",
)

response = client.chat("What is Python?")
print(f"Response: {response.content}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
```

### Streaming

```python
client = LLMClient(
    provider="google",
    model="gemini-1.5-pro",
    api_key="...",
)

def on_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Generate a list of ideas",
    on_chunk=on_chunk,
)
```

---

## Ollama (Local)

### Setup

1. **Install Ollama**
   - macOS: `brew install ollama`
   - Linux: Download from https://ollama.ai
   - Windows: Download from https://ollama.ai

2. **Download a Model**
   ```bash
   ollama pull llama2
   ollama pull mistral
   ollama pull neural-chat
   ```

3. **Start Ollama Server**
   ```bash
   ollama serve
   # Runs on http://localhost:11434
   ```

4. **Use in Socrates Nexus**
   ```python
   from socrates_nexus import LLMClient

   # No API key needed!
   client = LLMClient(
       provider="ollama",
       model="llama2",
       base_url="http://localhost:11434",
   )

   response = client.chat("Hello!")
   print(f"Cost: ${response.usage.cost_usd:.6f}")  # Free!
   ```

### Available Models

Popular models to download:

```bash
ollama pull llama2              # Meta's Llama 2
ollama pull mistral             # Mistral AI
ollama pull neural-chat         # Intel neural-chat
ollama pull orca-mini           # Orca Mini
ollama pull dolphin-mixtral     # Dolphin Mixtral
ollama pull openchat            # OpenChat
```

### Advantages

- ✅ **FREE** - No API costs
- ✅ **Private** - Runs locally, no data sent to external services
- ✅ **Offline** - Works without internet
- ✅ **Fast** - No network latency

### Disadvantages

- ❌ **Local compute** - Requires GPU for reasonable speed
- ❌ **Less powerful** - Open models are weaker than Claude/GPT-4
- ❌ **Manual setup** - Requires local installation

### Example Usage

```python
from socrates_nexus import LLMClient

# Using local Llama 2
client = LLMClient(
    provider="ollama",
    model="llama2",
)

response = client.chat("What is machine learning?")
print(response.content)

# Check cost (should be $0.00)
print(f"Cost: ${response.usage.cost_usd:.6f}")

# Streaming
def print_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Write a poem",
    on_chunk=print_chunk,
)
```

### Custom Ollama Port

If Ollama is running on a different port:

```python
client = LLMClient(
    provider="ollama",
    model="llama2",
    base_url="http://localhost:11435",  # Custom port
)
```

---

## Provider Comparison

### Speed (Fastest → Slowest)

1. **GPT-3.5-turbo** - Very fast
2. **Mistral** (Ollama) - Very fast
3. **Claude Haiku** - Fast
4. **Claude Sonnet** - Medium
5. **GPT-4** - Slower
6. **Claude Opus** - Slowest

### Cost (Cheapest → Most Expensive)

1. **Ollama** - FREE (local)
2. **Claude Haiku** - $0.80 / 1M input
3. **Gemini Flash** - Free tier / low cost
4. **GPT-3.5** - $0.50 / 1M input
5. **Claude Sonnet** - $3.00 / 1M input
6. **GPT-4** - $30.00 / 1M input
7. **Claude Opus** - $15.00 / 1M input

### Quality (Best Reasoning → Adequate)

1. **Claude Opus** - Best reasoning
2. **GPT-4** - Excellent
3. **Claude Sonnet** - Very good
4. **GPT-4-turbo** - Very good
5. **Gemini Pro** - Good
6. **Claude Haiku** - Good
7. **GPT-3.5** - Adequate
8. **Mistral** - Adequate
9. **Llama 2** - Basic

### Best Use Cases

| Use Case | Recommended |
|----------|-------------|
| **Most cost-effective** | Claude Haiku |
| **Best quality/cost** | Claude Sonnet |
| **Highest quality** | Claude Opus |
| **Free/private** | Ollama (local) |
| **Open source** | Mistral or Llama 2 (Ollama) |
| **Very large context** | Gemini 1.5 Pro (1M tokens) |

---

## Switching Providers

Socrates Nexus provides a unified API, so switching providers is easy:

```python
from socrates_nexus import LLMClient

# One-liner to switch providers
PROVIDER = "anthropic"  # Change to "openai", "google", "ollama"

client = LLMClient(
    provider=PROVIDER,
    model="claude-opus" if PROVIDER == "anthropic" else "gpt-4",
    api_key="...",
)

response = client.chat("Hello!")
```

---

## Provider Aliases

Socrates Nexus supports common aliases:

```python
# These all work:
LLMClient(provider="anthropic", model="claude-opus")
LLMClient(provider="claude", model="claude-opus")      # Alias

LLMClient(provider="openai", model="gpt-4")
LLMClient(provider="gpt", model="gpt-4")               # Alias

LLMClient(provider="google", model="gemini-pro")
LLMClient(provider="gemini", model="gemini-pro")       # Alias

LLMClient(provider="ollama", model="llama2")
LLMClient(provider="local", model="llama2")            # Alias
```

---

## Troubleshooting

### "API key not found"

Make sure your API key is set:

```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Or pass it directly
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="sk-ant-...",
)
```

### "Connection refused" (Ollama)

Make sure Ollama is running:

```bash
# Check if running
curl http://localhost:11434

# If not, start it
ollama serve
```

### "Model not found"

Make sure the model exists and you've pulled it (for Ollama):

```bash
# For Ollama
ollama pull llama2

# For others, check available models in the table above
```

### "Rate limited"

Socrates Nexus automatically retries. To customize:

```python
client = LLMClient(
    provider="anthropic",
    model="claude-opus",
    api_key="...",
    retry_attempts=5,
    retry_backoff_factor=3.0,
)
```

---

## Next Steps

- Read [Quick Start](quickstart.md) for basic usage
- See [Advanced Usage](advanced.md) for callbacks and monitoring
- Check [examples/](../examples/) for complete examples
