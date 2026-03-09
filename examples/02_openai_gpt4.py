"""
Example 2: OpenAI GPT-4 with Streaming

Demonstrates real-time streaming responses from OpenAI.
"""

import os
from socrates_nexus import LLMClient

# Initialize OpenAI client
client = LLMClient(
    provider="openai",
    model="gpt-4o",  # or gpt-4, gpt-3.5-turbo
    api_key=os.getenv("OPENAI_API_KEY"),
)

print("=" * 60)
print("OPENAI GPT-4 - STREAMING RESPONSE")
print("=" * 60)
print("\nStreaming response (real-time chunks):\n")

# Define callback for each chunk
def on_chunk(chunk: str):
    """Print each chunk as it arrives."""
    print(chunk, end="", flush=True)

# Stream response with callback
response = client.stream(
    "Write a haiku about artificial intelligence",
    on_chunk=on_chunk,
)

print("\n\n--- Usage Stats ---")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
print(f"Latency: {response.usage.latency_ms:.2f}ms")
