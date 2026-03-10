"""
Example: Using Vision Models with Socrates Nexus

Demonstrates how to use vision models (Claude 3 Vision, GPT-4V, etc.) to analyze images.

Installation:
    pip install socrates-nexus[all]

Requires:
    - API key for your chosen provider (ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY)
    - An image file or URL to analyze
"""

from socrates_nexus import LLMClient


def example_vision_with_url():
    """Analyze an image from a URL."""
    print("=== Vision Model with Image URL ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    # Analyze an image from a URL
    response = client.chat(
        "What's in this image? Describe the main elements.",
        images=["https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"]
    )

    print(f"Response: {response.content}\n")


def example_vision_with_file():
    """Analyze an image from a local file."""
    print("=== Vision Model with Local File ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    try:
        # Analyze a local image file
        response = client.chat(
            "What objects are visible in this image?",
            images=["./sample_image.jpg"]  # Replace with your image file
        )

        print(f"Response: {response.content}\n")
    except FileNotFoundError:
        print("Sample image not found. Please provide a valid image path.\n")


def example_multiple_images():
    """Compare multiple images."""
    print("=== Comparing Multiple Images ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    response = client.chat(
        "Compare these two images and describe the differences.",
        images=[
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/YellowLabradorLooking_new.jpg/1200px-YellowLabradorLooking_new.jpg"
        ]
    )

    print(f"Response: {response.content}\n")


def example_provider_comparison():
    """Use vision with different providers."""
    print("=== Provider Comparison ===\n")

    providers = ["anthropic", "openai", "google"]
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"

    for provider in providers:
        try:
            if provider == "anthropic":
                model = "claude-3-5-sonnet"
            elif provider == "openai":
                model = "gpt-4-vision"
            else:  # google
                model = "gemini-1.5-pro-vision"

            client = LLMClient(provider=provider, model=model)
            response = client.chat(
                "Briefly describe what you see in this image.",
                images=[image_url]
            )

            print(f"{provider.upper()}:")
            print(f"  Model: {model}")
            print(f"  Response: {response.content}\n")

        except Exception as e:
            print(f"{provider.upper()}: Error - {str(e)}\n")


def example_vision_with_follow_up():
    """Ask follow-up questions about an image."""
    print("=== Vision with Follow-up Questions ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"

    # Initial analysis
    response1 = client.chat(
        "What animal is in this image?",
        images=[image_url]
    )
    print(f"Q1: What animal is in this image?")
    print(f"A1: {response1.content}\n")

    # Follow-up question (note: each call is independent, so we include the image again)
    response2 = client.chat(
        "What is the color of the animal?",
        images=[image_url]
    )
    print(f"Q2: What is the color of the animal?")
    print(f"A2: {response2.content}\n")


if __name__ == "__main__":
    print("Socrates Nexus Vision Models Examples\n")
    print("=" * 50 + "\n")

    try:
        example_vision_with_url()
        example_multiple_images()
        example_provider_comparison()
        example_vision_with_follow_up()

    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install required dependencies:")
        print("  pip install socrates-nexus[all]")
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nMake sure you have set up your API keys:")
        print("  - ANTHROPIC_API_KEY for Claude models")
        print("  - OPENAI_API_KEY for GPT-4 Vision")
        print("  - GOOGLE_API_KEY for Gemini Vision")
