"""Base provider interface for Socrates Nexus."""

import hashlib
from abc import ABC, abstractmethod
from typing import Optional, Callable

from ..models import ChatResponse, TokenUsage, LLMConfig, PROVIDER_PRICING
from ..exceptions import ProviderError


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: LLMConfig):
        """
        Initialize provider with configuration.

        Args:
            config: LLM configuration
        """
        self.config = config
        self.name = self.__class__.__name__
        self.pricing = PROVIDER_PRICING.get(config.provider, {})
        self._usage_callbacks: list[Callable[[TokenUsage], None]] = []

    @abstractmethod
    def chat(self, message: str, **kwargs) -> ChatResponse:
        """
        Send a chat message and get response.

        Args:
            message: User message
            **kwargs: Additional provider-specific arguments

        Returns:
            ChatResponse with content and usage information
        """
        pass

    @abstractmethod
    async def achat(self, message: str, **kwargs) -> ChatResponse:
        """Async version of chat."""
        pass

    @abstractmethod
    def stream(self, message: str, on_chunk: Callable[[str], None], **kwargs) -> ChatResponse:
        """
        Stream a chat response with callback.

        Args:
            message: User message
            on_chunk: Callback function for each chunk
            **kwargs: Additional provider-specific arguments

        Returns:
            ChatResponse with complete content and usage
        """
        pass

    @abstractmethod
    async def astream(
        self, message: str, on_chunk: Callable[[str], None], **kwargs
    ) -> ChatResponse:
        """Async version of stream."""
        pass

    def calculate_cost(
        self, input_tokens: int, output_tokens: int, model: Optional[str] = None
    ) -> float:
        """
        Calculate cost for token usage.

        Extracted from Socrates ClaudeClient pattern (lines 1709-1718).

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name (uses config model if None)

        Returns:
            Cost in USD
        """
        model = model or self.config.model
        pricing = self.pricing.get(model, {})

        if not pricing:
            return 0.0

        # Pricing is per million tokens, stored as cost per 1M
        input_cost = (input_tokens / 1_000_000) * pricing.get("input", 0.0)
        output_cost = (output_tokens / 1_000_000) * pricing.get("output", 0.0)

        return round(input_cost + output_cost, 6)

    def add_usage_callback(self, callback: Callable[[TokenUsage], None]) -> None:
        """
        Add callback for token usage tracking.

        Replaces orchestrator event emission pattern with pluggable callbacks.

        Args:
            callback: Function to call with TokenUsage
        """
        self._usage_callbacks.append(callback)

    def _notify_usage(self, usage: TokenUsage) -> None:
        """
        Notify all registered callbacks of token usage.

        Args:
            usage: Token usage information
        """
        for callback in self._usage_callbacks:
            try:
                callback(usage)
            except Exception:
                # Don't fail on callback errors
                pass

    def _generate_cache_key(self, message: str) -> str:
        """
        Generate SHA256 cache key for message.

        Extracted from Socrates ClaudeClient pattern (lines 1674-1676).

        Args:
            message: Message to generate key for

        Returns:
            SHA256 hex digest
        """
        return hashlib.sha256(message.encode()).hexdigest()

    def _create_token_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float = 0.0,
    ) -> TokenUsage:
        """
        Create TokenUsage object with calculated cost.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            latency_ms: Request latency in milliseconds

        Returns:
            TokenUsage object with cost calculated
        """
        cost = self.calculate_cost(input_tokens, output_tokens)

        return TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=cost,
            provider=self.config.provider,
            model=self.config.model,
            latency_ms=latency_ms,
        )

    def _handle_api_error(self, error: Exception, operation: str) -> None:
        """
        Convert provider-specific errors to Nexus exceptions.

        To be implemented by subclasses for provider-specific error handling.

        Args:
            error: Original provider error
            operation: Operation that failed (e.g., "chat", "stream")

        Raises:
            ProviderError: Converted error
        """
        raise ProviderError(
            f"{operation} failed with {self.config.provider}: {str(error)}",
            error_code=f"{self.config.provider.upper()}_ERROR",
        )

    def __repr__(self) -> str:
        return f"{self.name}(model={self.config.model})"
