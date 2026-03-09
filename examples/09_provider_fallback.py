"""
Example 9: Provider Fallback and Multi-Model Resilience

Demonstrates fallback strategies when a provider fails:
- Sequential fallback: try provider 1, then provider 2
- Parallel fallback: try multiple providers concurrently, use first successful
- Model-specific fallback: if Claude fails, try GPT-4
"""

import asyncio
import os
from socrates_nexus import LLMClient, AsyncLLMClient, NexusError

print("=" * 60)
print("PROVIDER FALLBACK - SEQUENTIAL FALLBACK")
print("=" * 60)


def safe_chat_sequential(message: str, providers_config: list) -> dict:
    """Try each provider in sequence until one succeeds."""
    results = {
        "message": message,
        "attempts": [],
        "success": False,
        "response": None,
        "provider_used": None,
        "error": None,
    }

    for config in providers_config:
        provider = config["provider"]
        model = config["model"]
        api_key = config.get("api_key")

        try:
            print(f"\nAttempting with {provider} ({model})...")

            client = LLMClient(
                provider=provider,
                model=model,
                api_key=api_key,
            )

            response = client.chat(message)

            results["attempts"].append(
                {
                    "provider": provider,
                    "status": "success",
                    "cost": response.usage.cost_usd,
                }
            )
            results["success"] = True
            results["response"] = response.content
            results["provider_used"] = provider
            print(f"  ✓ Success!")
            break

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:50]}"
            results["attempts"].append(
                {
                    "provider": provider,
                    "status": "failed",
                    "error": error_msg,
                }
            )
            print(f"  ✗ Failed: {error_msg}")
            results["error"] = str(e)

    return results


# Test sequential fallback
print("\nTesting Sequential Fallback (invalid API key first, then real):\n")

providers = [
    {
        "provider": "anthropic",
        "model": "claude-haiku-4-5-20251001",
        "api_key": "invalid-key",
    },
    {
        "provider": "anthropic",
        "model": "claude-haiku-4-5-20251001",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
]

result = safe_chat_sequential("What is machine learning?", providers)

print("\n--- Sequential Fallback Result ---")
print(f"Message: {result['message'][:50]}...")
print(f"Success: {result['success']}")
print(f"Provider Used: {result['provider_used']}")
print(f"Attempts: {len(result['attempts'])}")
for i, attempt in enumerate(result["attempts"], 1):
    status = "✓" if attempt["status"] == "success" else "✗"
    print(
        f"  {i}. {attempt['provider']}: {attempt['status']} "
        f"({attempt.get('cost', attempt.get('error'))})"
    )

# Example 2: Parallel fallback with asyncio
print("\n" + "=" * 60)
print("PROVIDER FALLBACK - PARALLEL FALLBACK")
print("=" * 60)


async def chat_with_provider(provider: str, model: str, api_key, message: str):
    """Attempt a chat request with given provider."""
    client = AsyncLLMClient(
        provider=provider,
        model=model,
        api_key=api_key,
    )

    response = await client.chat(message)
    return {
        "provider": provider,
        "model": model,
        "content": response.content,
        "cost": response.usage.cost_usd,
        "tokens": response.usage.total_tokens,
    }


async def safe_chat_parallel(message: str, providers_config: list):
    """Try multiple providers in parallel, return first successful."""
    print(f"\nAttempting {len(providers_config)} providers in parallel...")

    tasks = [
        chat_with_provider(
            config["provider"],
            config["model"],
            config.get("api_key"),
            message,
        )
        for config in providers_config
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Find first successful result
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  ✗ Provider {i+1}: {type(result).__name__}")
        else:
            print(
                f"  ✓ Provider {i+1} ({result['provider']}): Success! "
                f"({result['tokens']} tokens, ${result['cost']:.6f})"
            )

    # Return first non-exception result
    for result in results:
        if not isinstance(result, Exception):
            return result

    # All failed
    return None


print("\nTesting Parallel Fallback (multiple providers at once):\n")

# Configure multiple providers to try in parallel
multi_providers = [
    {
        "provider": "anthropic",
        "model": "claude-haiku-4-5-20251001",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
]

# Run parallel fallback
parallel_result = asyncio.run(
    safe_chat_parallel("What is artificial intelligence?", multi_providers)
)

if parallel_result:
    print("\n--- Parallel Fallback Result ---")
    print(f"Provider Used: {parallel_result['provider']}")
    print(f"Model: {parallel_result['model']}")
    print(f"Response: {parallel_result['content'][:100]}...")
    print(f"Cost: ${parallel_result['cost']:.6f}")
else:
    print("\n--- Parallel Fallback Result ---")
    print("All providers failed")

# Example 3: Model-specific fallback strategy
print("\n" + "=" * 60)
print("PROVIDER FALLBACK - MODEL-SPECIFIC FALLBACK")
print("=" * 60)


def get_response_with_model_fallback(message: str) -> dict:
    """Try progressively more powerful models if one fails or is rate-limited."""

    model_chain = [
        {
            "provider": "anthropic",
            "model": "claude-haiku-4-5-20251001",
            "description": "Fast & cheap",
        },
        {
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "description": "Balanced (faster Sonnet)",
        },
        {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "description": "Fast OpenAI fallback",
        },
        {
            "provider": "openai",
            "model": "gpt-4",
            "description": "Most powerful (expensive)",
        },
    ]

    print(f"\nStrategy: Try models in order, escalating if needed\n")

    for i, model_config in enumerate(model_chain, 1):
        provider = model_config["provider"]
        model = model_config["model"]
        description = model_config["description"]

        try:
            print(f"{i}. Trying {model} ({description})...", end=" ")

            client = LLMClient(
                provider=provider,
                model=model,
                api_key=os.getenv(
                    "ANTHROPIC_API_KEY"
                    if provider == "anthropic"
                    else "OPENAI_API_KEY"
                ),
            )

            response = client.chat(message)

            print(
                f"✓ Success! ({response.usage.total_tokens} tokens, "
                f"${response.usage.cost_usd:.6f})"
            )

            return {
                "success": True,
                "model": model,
                "provider": provider,
                "content": response.content,
                "cost": response.usage.cost_usd,
                "tokens": response.usage.total_tokens,
                "attempts": i,
            }

        except Exception as e:
            error_type = type(e).__name__
            print(f"✗ {error_type}")

    return {
        "success": False,
        "error": "All models failed",
        "attempts": len(model_chain),
    }


print("\nTesting Model-Specific Fallback:\n")

fallback_result = get_response_with_model_fallback("Explain quantum computing briefly")

print("\n--- Model Fallback Result ---")
if fallback_result["success"]:
    print(f"Success after {fallback_result['attempts']} attempt(s)")
    print(f"Model Used: {fallback_result['model']} ({fallback_result['provider']})")
    print(f"Response: {fallback_result['content'][:100]}...")
    print(f"Total Cost: ${fallback_result['cost']:.6f}")
else:
    print(f"Failed: {fallback_result['error']}")

# Example 4: Intelligent fallback with cost optimization
print("\n" + "=" * 60)
print("PROVIDER FALLBACK - COST-OPTIMIZED FALLBACK")
print("=" * 60)


def chat_with_cost_fallback(
    message: str, max_cost: float = 0.01
) -> dict:
    """Try models in order of cost-efficiency."""

    cost_optimized_chain = [
        {
            "provider": "anthropic",
            "model": "claude-haiku-4-5-20251001",
            "estimated_cost_per_1k": 0.00080,
            "description": "Cheapest - Haiku",
        },
        {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "estimated_cost_per_1k": 0.00150,
            "description": "Very cheap - GPT-3.5",
        },
        {
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "estimated_cost_per_1k": 0.00300,
            "description": "Moderate - Sonnet",
        },
    ]

    print(f"\nStrategy: Use cheapest model that fits budget (max ${max_cost})\n")

    for config in cost_optimized_chain:
        provider = config["provider"]
        model = config["model"]
        description = config["description"]
        est_cost = config["estimated_cost_per_1k"]

        try:
            print(
                f"Trying {description} (est. ${est_cost * 1000:.4f}/1M tokens)...",
                end=" ",
            )

            client = LLMClient(
                provider=provider,
                model=model,
                api_key=os.getenv(
                    "ANTHROPIC_API_KEY"
                    if provider == "anthropic"
                    else "OPENAI_API_KEY"
                ),
            )

            response = client.chat(message)

            actual_cost = response.usage.cost_usd

            if actual_cost <= max_cost:
                print(
                    f"✓ Within budget! (${actual_cost:.6f})"
                )
                return {
                    "success": True,
                    "model": model,
                    "provider": provider,
                    "cost": actual_cost,
                    "within_budget": True,
                }
            else:
                print(
                    f"✗ Over budget (${actual_cost:.6f} > ${max_cost:.6f})"
                )

        except Exception as e:
            print(f"✗ {type(e).__name__}")

    return {
        "success": False,
        "error": "No model within budget",
    }


print("\nTesting Cost-Optimized Fallback:\n")

cost_result = chat_with_cost_fallback("What is Python?", max_cost=0.01)

print("\n--- Cost Fallback Result ---")
if cost_result["success"]:
    print(f"Model Used: {cost_result['model']} ({cost_result['provider']})")
    print(f"Actual Cost: ${cost_result['cost']:.6f}")
    print(f"Within Budget: {cost_result['within_budget']}")
else:
    print(f"Failed: {cost_result['error']}")

print("\n" + "=" * 60)
print("FALLBACK PATTERNS COMPLETE")
print("=" * 60)
