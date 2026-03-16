"""DigitalOcean Gradient™ AI LLM provider.

Uses the official ``gradient`` Python SDK for both Serverless Inference
and Agent Inference on DigitalOcean's Gradient AI Platform.

Environment variables:
    GRADIENT_MODEL_ACCESS_KEY  – for serverless inference (direct model calls)
    GRADIENT_AGENT_ACCESS_KEY  – for agent inference (managed agents)
    GRADIENT_AGENT_ENDPOINT    – agent endpoint URL (required for agent mode)

Docs: https://gradient-sdk.digitalocean.com/getting-started/overview
"""

from __future__ import annotations

import logging
import os
from collections.abc import AsyncIterator
from typing import Any

from framework.llm.provider import LLMProvider, LLMResponse, Tool
from framework.llm.stream_events import (
    FinishEvent,
    StreamEvent,
    TextDeltaEvent,
    TextEndEvent,
)

logger = logging.getLogger(__name__)

# Default model for serverless inference when none specified
DEFAULT_GRADIENT_MODEL = "llama3.3-70b-instruct"


class GradientProvider(LLMProvider):
    """LLM provider backed by DigitalOcean Gradient™ AI Platform.

    Supports two modes:
    - **Serverless Inference**: direct model calls via GRADIENT_MODEL_ACCESS_KEY
    - **Agent Inference**: managed agent calls via GRADIENT_AGENT_ACCESS_KEY
    """

    def __init__(
        self,
        model: str | None = None,
        model_access_key: str | None = None,
        agent_access_key: str | None = None,
        agent_endpoint: str | None = None,
        temperature: float = 0.7,
    ):
        self.model = model or DEFAULT_GRADIENT_MODEL
        self.temperature = temperature

        # Resolve keys from env if not passed directly
        self._model_access_key = model_access_key or os.environ.get("GRADIENT_MODEL_ACCESS_KEY")
        self._agent_access_key = agent_access_key or os.environ.get("GRADIENT_AGENT_ACCESS_KEY")
        self._agent_endpoint = agent_endpoint or os.environ.get("GRADIENT_AGENT_ENDPOINT")

        # Determine mode: agent inference takes priority if both keys present
        self._use_agent_mode = bool(self._agent_access_key and self._agent_endpoint)

        self._sync_client: Any = None
        self._async_client: Any = None

    def _get_sync_client(self) -> Any:
        """Lazy-init the sync Gradient client."""
        if self._sync_client is None:
            try:
                from gradient import Gradient
            except ImportError as exc:
                raise ImportError("Install the Gradient SDK: pip install gradient") from exc

            if self._use_agent_mode:
                self._sync_client = Gradient(
                    agent_access_key=self._agent_access_key,
                    agent_endpoint=self._agent_endpoint,
                )
            else:
                self._sync_client = Gradient(
                    model_access_key=self._model_access_key,
                )
        return self._sync_client

    def _get_async_client(self) -> Any:
        """Lazy-init the async Gradient client."""
        if self._async_client is None:
            try:
                from gradient import AsyncGradient
            except ImportError as exc:
                raise ImportError("Install the Gradient SDK: pip install gradient") from exc

            if self._use_agent_mode:
                self._async_client = AsyncGradient(
                    agent_access_key=self._agent_access_key,
                    agent_endpoint=self._agent_endpoint,
                )
            else:
                self._async_client = AsyncGradient(
                    model_access_key=self._model_access_key,
                )
        return self._async_client

    def _build_messages(
        self,
        messages: list[dict[str, Any]],
        system: str = "",
    ) -> list[dict[str, Any]]:
        """Prepend system prompt as a system message if provided."""
        out: list[dict[str, Any]] = []
        if system:
            out.append({"role": "system", "content": system})
        out.extend(messages)
        return out

    # ------------------------------------------------------------------
    # Sync completion
    # ------------------------------------------------------------------

    def complete(
        self,
        messages: list[dict[str, Any]],
        system: str = "",
        tools: list[Tool] | None = None,
        max_tokens: int = 1024,
        response_format: dict[str, Any] | None = None,
        json_mode: bool = False,
        max_retries: int | None = None,
    ) -> LLMResponse:
        client = self._get_sync_client()
        built = self._build_messages(messages, system)

        kwargs: dict[str, Any] = {
            "messages": built,
            "model": self.model,
        }
        # Agent mode ignores model param on the server side, but SDK requires it
        if self._use_agent_mode:
            kwargs["model"] = "ignored"

        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = client.chat.completions.create(**kwargs)
        except Exception:
            # Fall back to agent endpoint if available
            if not self._use_agent_mode and self._agent_access_key:
                logger.warning("Serverless inference failed, trying agent mode")
                response = client.agents.chat.completions.create(**kwargs)
            else:
                raise

        choice = response.choices[0]
        usage = getattr(response, "usage", None)

        return LLMResponse(
            content=choice.message.content or "",
            model=getattr(response, "model", self.model),
            input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
            output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
            stop_reason=getattr(choice, "finish_reason", "stop") or "stop",
            raw_response=response,
        )

    # ------------------------------------------------------------------
    # Async completion
    # ------------------------------------------------------------------

    async def acomplete(
        self,
        messages: list[dict[str, Any]],
        system: str = "",
        tools: list[Tool] | None = None,
        max_tokens: int = 1024,
        response_format: dict[str, Any] | None = None,
        json_mode: bool = False,
        max_retries: int | None = None,
    ) -> LLMResponse:
        client = self._get_async_client()
        built = self._build_messages(messages, system)

        kwargs: dict[str, Any] = {
            "messages": built,
            "model": self.model,
        }
        if self._use_agent_mode:
            kwargs["model"] = "ignored"
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = await client.chat.completions.create(**kwargs)
        except Exception:
            if not self._use_agent_mode and self._agent_access_key:
                logger.warning("Serverless inference failed, trying agent mode")
                response = await client.agents.chat.completions.create(**kwargs)
            else:
                raise

        choice = response.choices[0]
        usage = getattr(response, "usage", None)

        return LLMResponse(
            content=choice.message.content or "",
            model=getattr(response, "model", self.model),
            input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
            output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
            stop_reason=getattr(choice, "finish_reason", "stop") or "stop",
            raw_response=response,
        )

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    async def stream(
        self,
        messages: list[dict[str, Any]],
        system: str = "",
        tools: list[Tool] | None = None,
        max_tokens: int = 4096,
    ) -> AsyncIterator[StreamEvent]:
        """Stream via Gradient SDK with SSE support."""
        client = self._get_async_client()
        built = self._build_messages(messages, system)

        kwargs: dict[str, Any] = {
            "messages": built,
            "model": self.model,
            "stream": True,
        }
        if self._use_agent_mode:
            kwargs["model"] = "ignored"
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        try:
            stream = await client.chat.completions.create(**kwargs)
        except Exception:
            # Fallback: non-streaming completion wrapped as synthetic events
            response = await self.acomplete(
                messages=messages, system=system, tools=tools, max_tokens=max_tokens
            )
            yield TextDeltaEvent(content=response.content, snapshot=response.content)
            yield TextEndEvent(full_text=response.content)
            yield FinishEvent(
                stop_reason=response.stop_reason,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                model=response.model,
            )
            return

        full_text = ""
        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None) or ""
            if content:
                full_text += content
                yield TextDeltaEvent(content=content, snapshot=full_text)

        yield TextEndEvent(full_text=full_text)
        yield FinishEvent(
            stop_reason="stop",
            input_tokens=0,
            output_tokens=0,
            model=self.model,
        )
