"""
Example 6: Async/Await and Concurrent Requests

Demonstrates asynchronous usage and parallel requests to multiple models.
"""

import asyncio
import os
from socrates_nexus import AsyncLLMClient

print("=" * 60)
print("ASYNC - EXAMPLE 1: Single Async Request")
print("=" * 60)


async def single_async_request():
    """Simple async request to Claude."""
    client = AsyncLLMClient(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    response = await client.chat("What is the speed of light?")

    print(f"Response: {response.content}")
    print(f"Cost: ${response.usage.cost_usd:.6f}")


asyncio.run(single_async_request())

# Example 2: Parallel requests to same provider
print("\n" + "=" * 60)
print("ASYNC - EXAMPLE 2: Parallel Requests (Same Provider)")
print("=" * 60)


async def parallel_same_provider():
    """Send multiple concurrent requests to the same provider."""
    client = AsyncLLMClient(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    # Launch all requests concurrently
    responses = await asyncio.gather(
        client.chat("What is Python?"),
        client.chat("What is JavaScript?"),
        client.chat("What is Rust?"),
    )

    total_cost = 0
    for i, response in enumerate(responses, 1):
        print(f"\nRequest {i}:")
        print(f"  Response: {response.content[:100]}...")
        print(f"  Cost: ${response.usage.cost_usd:.6f}")
        total_cost += response.usage.cost_usd

    print(f"\nTotal cost for 3 parallel requests: ${total_cost:.6f}")


asyncio.run(parallel_same_provider())

# Example 3: Multi-provider concurrent requests
print("\n" + "=" * 60)
print("ASYNC - EXAMPLE 3: Parallel Requests (Different Providers)")
print("=" * 60)


async def multi_provider_parallel():
    """Send requests to different providers in parallel."""

    # Create clients for different providers
    anthropic_client = AsyncLLMClient(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    openai_client = AsyncLLMClient(
        provider="openai",
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    google_client = AsyncLLMClient(
        provider="google",
        model="gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    try:
        # Send the same prompt to all three providers concurrently
        prompt = "Explain what an API is in one sentence"

        responses = await asyncio.gather(
            anthropic_client.chat(prompt),
            openai_client.chat(prompt),
            google_client.chat(prompt),
            return_exceptions=True,  # Don't fail if one provider errors
        )

        providers = ["Anthropic Claude", "OpenAI GPT", "Google Gemini"]

        total_cost = 0
        for provider_name, response in zip(providers, responses):
            if isinstance(response, Exception):
                print(f"\n{provider_name}: Error - {response}")
            else:
                print(f"\n{provider_name}:")
                print(f"  Response: {response.content[:80]}...")
                print(f"  Cost: ${response.usage.cost_usd:.6f}")
                total_cost += response.usage.cost_usd

        print(f"\nTotal cost across all 3 providers: ${total_cost:.6f}")

    except Exception as e:
        print(f"Error: {e}")
        print(
            "Make sure all API keys are set: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY"
        )


asyncio.run(multi_provider_parallel())
