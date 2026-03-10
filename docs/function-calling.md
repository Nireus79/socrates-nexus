# Function Calling Guide

Function calling (also known as tool use) enables LLMs to invoke predefined functions and integrate their results into responses. This guide shows you how to use function calling with Socrates Nexus.

## Overview

Function calling allows your LLM to:
- Call predefined functions to perform tasks
- Reason about which function to use for a given request
- Integrate function results into natural responses
- Handle multi-step workflows automatically

## Supported Providers

- **Anthropic Claude** - Native function calling support
- **OpenAI GPT-4 Turbo** - Tool use capabilities
- **Google Gemini** - Function calling support

## Basic Usage

### Define a Tool

```python
from socrates_nexus.models import Tool, Function

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
```

### Use the Tool in Chat

```python
from socrates_nexus import LLMClient

client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")

response = client.chat(
    "What's the weather in New York?",
    tools=[weather_tool]
)

# Check if the model called any tools
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

## Advanced Features

### Multiple Tools

Provide multiple tools for the model to choose from:

```python
tools = [
    weather_tool,
    calculator_tool,
    search_tool,
    database_tool
]

response = client.chat(
    "What's the weather in Paris and what's 15 plus 27?",
    tools=tools
)
```

### Tool Choice Modes

Control how the model uses tools:

```python
# Model decides whether to use tools (default)
response = client.chat(
    "What's the weather?",
    tools=[weather_tool],
    tool_choice="auto"
)

# Model must not use tools
response = client.chat(
    "Explain cloud computing",
    tools=[weather_tool],
    tool_choice="none"
)
```

### Implementing Tool Handlers

```python
import json

# In your application
def handle_tool_call(tool_call):
    """Execute a tool call and return the result."""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        return get_weather(arguments["location"])
    elif function_name == "calculate":
        return calculate(arguments)
    else:
        return {"error": f"Unknown function: {function_name}"}

# Process tool calls
response = client.chat("What's the weather in London?", tools=[weather_tool])
if response.tool_calls:
    for tool_call in response.tool_calls:
        result = handle_tool_call(tool_call)
        # In a real application, you'd send this result back to the model
        print(f"Tool result: {result}")
```

## Tool Definition Best Practices

### 1. Clear Descriptions

```python
# Good
Function(
    name="search_documents",
    description="Search through documents for specific content"
)

# Bad
Function(
    name="search",
    description="Search"
)
```

### 2. Detailed Parameters

```python
# Good
parameters={
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Search query (e.g., 'budget 2024')"
        },
        "document_type": {
            "type": "string",
            "enum": ["report", "memo", "email"],
            "description": "Type of document to search"
        }
    },
    "required": ["query"]
}

# Bad
parameters={"type": "object"}
```

### 3. Specify Required Parameters

Always mark parameters that must be provided:

```python
"required": ["location", "date"]  # These parameters are mandatory
```

## JSON Schema for Parameters

Function parameters use JSON Schema format:

```python
parameters={
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "User's name"
        },
        "age": {
            "type": "integer",
            "description": "User's age",
            "minimum": 0,
            "maximum": 150
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Associated tags"
        },
        "metadata": {
            "type": "object",
            "description": "Additional metadata"
        }
    },
    "required": ["name", "age"]
}
```

## Provider-Specific Details

### Anthropic Claude

- Models: `claude-3-5-sonnet`, `claude-3-opus`
- Native function calling support
- Automatic argument JSON parsing

### OpenAI GPT-4 Turbo

- Models: `gpt-4-turbo`, `gpt-4-vision`
- Full tool use support
- Reliable argument extraction

### Google Gemini

- Models: `gemini-1.5-pro`, `gemini-2.0-flash`
- Function calling support
- Efficient tool invocation

## Error Handling

```python
from socrates_nexus.exceptions import (
    InvalidRequestError,
    RateLimitError,
    ProviderError
)

try:
    response = client.chat(
        "Execute this operation",
        tools=[my_tool]
    )
except InvalidRequestError as e:
    print(f"Invalid tool definition: {e}")
except RateLimitError:
    print("Rate limited - wait before retrying")
except ProviderError as e:
    print(f"Provider error: {e}")
```

## Real-World Example

```python
def build_calculator_tools():
    """Create calculator tools."""
    return [
        Tool(
            function=Function(
                name="add",
                description="Add two numbers",
                parameters={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            )
        ),
        Tool(
            function=Function(
                name="multiply",
                description="Multiply two numbers",
                parameters={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            )
        )
    ]

# Use in application
client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")
tools = build_calculator_tools()

response = client.chat(
    "What's 25 times 4 plus 10?",
    tools=tools
)

print(f"Model response: {response.content}")
if response.tool_calls:
    print(f"Tool calls: {len(response.tool_calls)}")
    for tc in response.tool_calls:
        print(f"  - {tc.function.name}: {tc.function.arguments}")
```

## Performance Optimization

1. **Limit Tool Count** - Include only relevant tools
2. **Use tool_choice="none"** - When tools aren't needed
3. **Cache Responses** - For repeated operations

```python
client = LLMClient(
    provider="anthropic",
    model="claude-3-5-sonnet",
    cache_responses=True,
    cache_ttl=3600
)
```

## Examples

See full working examples in `examples/13_function_calling.py`

## API Reference

### Tool Model

```python
from socrates_nexus.models import Tool, Function

tool = Tool(
    type: Literal["function"] = "function"
    function: Function  # The function definition
)
```

### Function Model

```python
function = Function(
    name: str              # Function name
    description: str       # What the function does
    parameters: dict       # JSON Schema of parameters
)
```

### ToolCall Model

```python
tool_call = ToolCall(
    id: str               # Unique call identifier
    type: Literal["function"] = "function"
    function: FunctionCall  # The function being called
)
```

### FunctionCall Model

```python
function_call = FunctionCall(
    name: str             # Function name
    arguments: str        # JSON string of arguments
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not calling tools | Add clearer descriptions, ensure tool is relevant |
| Wrong parameters passed | Define parameters with clear descriptions and types |
| Tool call ignored | Use tool_choice="auto" to encourage tool use |
| Invalid JSON in arguments | Ensure all parameter types are properly defined |

## Support

For issues or questions, contact: Hermes_creative@proton.me
