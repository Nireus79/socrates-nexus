"""
Example 4: Ollama Local LLM

Demonstrates running models locally with Ollama (no API key needed).

Prerequisites:
  1. Install Ollama from https://ollama.ai
  2. Run: ollama pull llama2
  3. Run: ollama serve (starts on http://localhost:11434)
"""

from socrates_nexus import LLMClient

print("=" * 60)
print("OLLAMA LOCAL MODEL - NO API KEY REQUIRED")
print("=" * 60)

# Initialize Ollama client (no API key needed)
# Make sure Ollama is running: ollama serve
client = LLMClient(
    provider="ollama",
    model="llama2",  # or mistral, neural-chat, orca-mini
    base_url="http://localhost:11434",  # Default Ollama URL
)

print("\nSending request to local Ollama model...")

try:
    response = client.chat("What is the capital of France? Answer in one sentence.")

    print(f"\nModel: {response.model}")
    print(f"Provider: {response.provider}")
    print(f"\nResponse:\n{response.content}")
    print(f"\n--- Usage Stats ---")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")
    print(f"Cost: ${response.usage.cost_usd:.6f} (local models are FREE!)")
    print(f"Latency: {response.usage.latency_ms:.2f}ms")

except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure Ollama is running:")
    print("  1. ollama pull llama2")
    print("  2. ollama serve")
