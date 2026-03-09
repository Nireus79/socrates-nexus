"""
Socrates Nexus - LangChain Integration

Provides LangChain-compatible LLM provider with multi-provider support.

Installation:
    pip install socrates-nexus[langchain]
"""

try:
    from .llm import SocratesNexusLLM
    __all__ = ["SocratesNexusLLM"]
except ImportError as e:
    if "langchain" in str(e):
        raise ImportError(
            "LangChain integration requires langchain. "
            "Install with: pip install socrates-nexus[langchain]"
        ) from e
    raise
