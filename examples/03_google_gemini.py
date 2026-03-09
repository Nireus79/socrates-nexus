"""
Example 3: Google Gemini

Demonstrates using Google's Gemini models through Socrates Nexus.
"""

import os
from socrates_nexus import LLMClient

# Initialize Google Gemini client
client = LLMClient(
    provider="google",
    model="gemini-1.5-flash",  # or gemini-1.5-pro
    api_key=os.getenv("GOOGLE_API_KEY"),
)

print("=" * 60)
print("GOOGLE GEMINI - BASIC USAGE")
print("=" * 60)

# Simple chat
response = client.chat("List 3 benefits of cloud computing in bullet points")

print(f"\nModel: {response.model}")
print(f"Provider: {response.provider}")
print(f"\nResponse:\n{response.content}")
print(f"\n--- Usage Stats ---")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Cost: ${response.usage.cost_usd:.6f}")
print(f"Latency: {response.usage.latency_ms:.2f}ms")

# Stream example
print("\n" + "=" * 60)
print("GOOGLE GEMINI - STREAMING")
print("=" * 60)
print("\nStreaming response:\n")

def on_chunk(chunk: str):
    print(chunk, end="", flush=True)

response = client.stream(
    "Explain quantum computing briefly",
    on_chunk=on_chunk,
)

print(f"\n\nTotal cost: ${response.usage.cost_usd:.6f}")
