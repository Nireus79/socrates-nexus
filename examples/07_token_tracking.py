"""
Example 7: Token Tracking and Cost Monitoring

Demonstrates tracking token usage and costs across requests.
"""

import os
from socrates_nexus import LLMClient, TokenUsage

print("=" * 60)
print("TOKEN TRACKING - BASIC USAGE STATISTICS")
print("=" * 60)

# Create client
client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Send multiple requests
queries = [
    "What is machine learning?",
    "Explain neural networks",
    "What is deep learning?",
]

print("\nSending 3 requests...\n")

for i, query in enumerate(queries, 1):
    response = client.chat(query)
    print(f"Request {i}: {response.usage.total_tokens} tokens, ${response.usage.cost_usd:.6f}")

# Get cumulative stats
stats = client.get_usage_stats()

print("\n" + "=" * 60)
print("CUMULATIVE STATISTICS")
print("=" * 60)
print(f"Total requests: {stats.total_requests}")
print(f"Total input tokens: {stats.total_input_tokens}")
print(f"Total output tokens: {stats.total_output_tokens}")
print(f"Total cost: ${stats.total_cost_usd:.6f}")

# Example 2: Custom usage tracking callback
print("\n" + "=" * 60)
print("TOKEN TRACKING - CUSTOM CALLBACKS")
print("=" * 60)

client2 = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Add custom callback to track usage
def track_usage_custom(usage: TokenUsage):
    """Custom callback that logs token usage."""
    efficiency = usage.output_tokens / max(usage.input_tokens, 1)
    print(
        f"  Usage: {usage.input_tokens} in → {usage.output_tokens} out "
        f"(efficiency: {efficiency:.2f}x) | Cost: ${usage.cost_usd:.6f}"
    )

# Register callback
client2.add_usage_callback(track_usage_custom)

print("\nRequests with custom tracking:\n")

client2.chat("What is Python?")
client2.chat("What is JavaScript?")

# Example 3: Track by provider and model
print("\n" + "=" * 60)
print("TOKEN TRACKING - BY PROVIDER AND MODEL")
print("=" * 60)

client3 = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

print("\nSending requests...\n")

for i in range(3):
    client3.chat(f"Tell me about topic {i+1}")

stats3 = client3.get_usage_stats()

print("\nBreakdown by Provider:")
for provider, provider_stats in stats3.by_provider.items():
    print(
        f"  {provider}: {provider_stats['requests']} requests, "
        f"{provider_stats['input_tokens']} input tokens, "
        f"${provider_stats['cost_usd']:.6f} total cost"
    )

print("\nBreakdown by Model:")
for model, model_stats in stats3.by_model.items():
    print(
        f"  {model}: {model_stats['requests']} requests, "
        f"${model_stats['cost_usd']:.6f} total cost"
    )
