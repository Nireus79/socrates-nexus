"""
Example 1: Basic Anthropic Claude Usage

Demonstrates the simplest way to use Socrates Nexus with Claude.
"""

import os
from socrates_nexus import LLMClient

# Initialize client with Claude
client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Simple chat - just send a message and get a response
response = client.chat("What is machine learning? Explain in 2 sentences.")

print("=" * 60)
print("ANTHROPIC CLAUDE - BASIC USAGE")
print("=" * 60)
print(f"\nModel: {response.model}")
print(f"Provider: {response.provider}")
print(f"\nResponse:\n{response.content}")
print(f"\n--- Usage Stats ---")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
print(f"Latency: {response.usage.latency_ms:.2f}ms")
