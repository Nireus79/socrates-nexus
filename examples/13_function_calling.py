"""
Example: Using Function Calling / Tool Use with Socrates Nexus

Demonstrates how to use function calling (tool use) to enable LLMs to call
predefined functions and get results integrated into their responses.

Installation:
    pip install socrates-nexus[all]

Requires:
    - API key for your chosen provider (ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY)
"""

from socrates_nexus import LLMClient
from socrates_nexus.models import Tool, Function, FunctionCall, ToolCall


def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get weather for a location. (Mock function)"""
    weather_data = {
        "New York": {"temperature": 15, "condition": "Cloudy"},
        "London": {"temperature": 10, "condition": "Rainy"},
        "Paris": {"temperature": 12, "condition": "Sunny"},
        "Tokyo": {"temperature": 20, "condition": "Clear"},
    }
    data = weather_data.get(location, {"temperature": 0, "condition": "Unknown"})
    if unit == "fahrenheit":
        data["temperature"] = int(data["temperature"] * 9/5 + 32)
    return data


def calculate(operation: str, a: float, b: float) -> float:
    """Perform a mathematical operation. (Mock function)"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else 0
    return 0


def example_basic_tool_use():
    """Basic function calling example."""
    print("=== Basic Function Calling ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    # Define a tool for getting weather
    weather_tool = Tool(
        function=Function(
            name="get_weather",
            description="Get the current weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        )
    )

    # Ask the model to use the tool
    response = client.chat(
        "What's the weather in London?",
        tools=[weather_tool]
    )

    print(f"Model response: {response.content}")
    if response.tool_calls:
        print(f"Tool calls made: {len(response.tool_calls)}")
        for tool_call in response.tool_calls:
            print(f"  - {tool_call.function.name}: {tool_call.function.arguments}")
    print()


def example_multiple_tools():
    """Function calling with multiple tools."""
    print("=== Multiple Function Calling ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    # Define multiple tools
    weather_tool = Tool(
        function=Function(
            name="get_weather",
            description="Get the current weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        )
    )

    calculator_tool = Tool(
        function=Function(
            name="calculate",
            description="Perform a mathematical operation",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Mathematical operation"
                    },
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["operation", "a", "b"]
            }
        )
    )

    # Ask the model to use multiple tools
    response = client.chat(
        "What's the weather in Paris and what's 15 plus 27?",
        tools=[weather_tool, calculator_tool]
    )

    print(f"Model response: {response.content}")
    if response.tool_calls:
        print(f"Tool calls made: {len(response.tool_calls)}")
        for tool_call in response.tool_calls:
            print(f"  - {tool_call.function.name}: {tool_call.function.arguments}")
    print()


def example_provider_comparison():
    """Function calling with different providers."""
    print("=== Provider Comparison ===\n")

    weather_tool = Tool(
        function=Function(
            name="get_weather",
            description="Get weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        )
    )

    providers = ["anthropic", "openai", "google"]

    for provider in providers:
        try:
            if provider == "anthropic":
                model = "claude-3-5-sonnet"
            elif provider == "openai":
                model = "gpt-4-turbo"
            else:  # google
                model = "gemini-1.5-pro"

            client = LLMClient(provider=provider, model=model)
            response = client.chat(
                "What's the weather in Tokyo?",
                tools=[weather_tool]
            )

            print(f"{provider.upper()}:")
            print(f"  Model: {model}")
            print(f"  Response: {response.content}")
            if response.tool_calls:
                print(f"  Tool calls: {len(response.tool_calls)}")
            print()

        except Exception as e:
            print(f"{provider.upper()}: Error - {str(e)}\n")


def example_tool_choice():
    """Function calling with different tool_choice modes."""
    print("=== Tool Choice Modes ===\n")

    client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

    weather_tool = Tool(
        function=Function(
            name="get_weather",
            description="Get weather for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        )
    )

    # tool_choice="auto" - model decides whether to use tools
    print("With tool_choice='auto':")
    response = client.chat(
        "What's the weather in New York?",
        tools=[weather_tool],
        tool_choice="auto"
    )
    print(f"  Response: {response.content}")
    print(f"  Tool calls: {len(response.tool_calls) if response.tool_calls else 0}\n")

    # tool_choice="none" - model doesn't use tools
    print("With tool_choice='none':")
    response = client.chat(
        "What's the weather in New York?",
        tools=[weather_tool],
        tool_choice="none"
    )
    print(f"  Response: {response.content}")
    print(f"  Tool calls: {len(response.tool_calls) if response.tool_calls else 0}\n")


if __name__ == "__main__":
    print("Socrates Nexus Function Calling Examples\n")
    print("=" * 50 + "\n")

    try:
        example_basic_tool_use()
        example_multiple_tools()
        example_provider_comparison()
        example_tool_choice()

    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install required dependencies:")
        print("  pip install socrates-nexus[all]")
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nMake sure you have set up your API keys:")
        print("  - ANTHROPIC_API_KEY for Claude models")
        print("  - OPENAI_API_KEY for GPT-4 Turbo")
        print("  - GOOGLE_API_KEY for Gemini models")
