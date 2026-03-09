"""
Example 5: Advanced Streaming with Custom Callbacks

Demonstrates different ways to handle streaming responses.
"""

import os
from socrates_nexus import LLMClient

# Use any provider you have API keys for
client = LLMClient(
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

print("=" * 60)
print("STREAMING - EXAMPLE 1: Print in Real-Time")
print("=" * 60)

def print_chunk(chunk: str):
    """Simple callback that prints each chunk."""
    print(chunk, end="", flush=True)

response = client.stream(
    "Count from 1 to 5, one number per line",
    on_chunk=print_chunk,
)

print(f"\n\nTotal cost: ${response.usage.cost_usd:.6f}\n")

# Example 2: Accumulate chunks with formatting
print("\n" + "=" * 60)
print("STREAMING - EXAMPLE 2: Accumulate and Format")
print("=" * 60)

chunks = []

def collect_chunk(chunk: str):
    """Collect chunks and track statistics."""
    chunks.append(chunk)
    # Show progress
    print(".", end="", flush=True)

response = client.stream(
    "Write a 3-sentence paragraph about renewable energy",
    on_chunk=collect_chunk,
)

full_response = "".join(chunks)
print(f"\n\nCollected {len(chunks)} chunks")
print(f"Total characters: {len(full_response)}")
print(f"Response:\n{full_response}")

# Example 3: Real-time token estimation
print("\n" + "=" * 60)
print("STREAMING - EXAMPLE 3: Track Streaming Progress")
print("=" * 60)

word_count = 0

def word_counter(chunk: str):
    """Track words as they stream."""
    global word_count
    word_count += len(chunk.split())
    print(f"[{word_count} words]", end=" ", flush=True)

response = client.stream(
    "List 5 types of machine learning algorithms",
    on_chunk=word_counter,
)

print(f"\n\nFinal word count: {word_count}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
