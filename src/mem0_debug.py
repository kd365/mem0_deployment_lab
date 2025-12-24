"""
Opt-in debug utilities for Mem0 LLM calls.

Goal: when infer=true behaves unexpectedly (e.g., empty results), allow capturing
the raw LLM response (especially from AWS Bedrock) so we can see whether it's:
- refusal / safety behavior
- non-JSON output
- unexpected JSON shape
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import contextvars


logger = logging.getLogger(__name__)


# Per-request context (so logs can be correlated back to a user_id/run_id)
mem0_request_context: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar(
    "mem0_request_context", default={}
)


def set_mem0_request_context(ctx: Dict[str, Any]) -> contextvars.Token:
    """Set context for the current request and return a token for resetting."""
    return mem0_request_context.set(ctx)


def reset_mem0_request_context(token: contextvars.Token) -> None:
    """Reset context to previous value using token returned by set_mem0_request_context()."""
    mem0_request_context.reset(token)


def _safe_truncate(s: str, limit: int) -> str:
    if limit <= 0:
        return ""
    if len(s) <= limit:
        return s
    return s[:limit] + "...(truncated)"


def _safe_json(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)


@dataclass
class DebugLlmProxy:
    """
    Proxy wrapper around Mem0's llm object.

    It logs raw responses when MEM0_DEBUG_LLM=1.
    """

    inner: Any
    provider: str
    model: str

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format: Optional[Union[str, Dict[str, Any]]] = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[str, Dict[str, Any]]:
        debug_enabled = os.getenv("MEM0_DEBUG_LLM", "").strip().lower() in {"1", "true", "yes"}
        include_prompts = os.getenv("MEM0_DEBUG_LLM_INCLUDE_PROMPTS", "").strip().lower() in {"1", "true", "yes"}
        max_chars = int(os.getenv("MEM0_DEBUG_LLM_MAX_CHARS", "1800"))

        # Heuristic: Bedrock infer issues are what we care about; keep logs quiet otherwise.
        should_log = debug_enabled and self.provider.lower() in {"aws_bedrock", "bedrock", "aws"}

        ctx = mem0_request_context.get({})
        ctx_safe = {
            "user_id": ctx.get("user_id"),
            "agent_id": ctx.get("agent_id"),
            "run_id": ctx.get("run_id"),
            "infer": ctx.get("infer"),
            "endpoint": ctx.get("endpoint"),
        }

        if should_log:
            logger.warning(
                "[MEM0_DEBUG_LLM] request provider=%s model=%s ctx=%s response_format=%s tools=%s stream=%s",
                self.provider,
                self.model,
                _safe_json(ctx_safe),
                _safe_json(response_format),
                "yes" if tools else "no",
                stream,
            )
            if include_prompts:
                # Redact nothing here (no secrets should be in prompts), but keep bounded.
                logger.warning(
                    "[MEM0_DEBUG_LLM] messages=%s",
                    _safe_truncate(_safe_json(messages), max_chars),
                )

        try:
            resp = self.inner.generate_response(
                messages=messages,
                response_format=response_format,
                tools=tools,
                tool_choice=tool_choice,
                stream=stream,
                **kwargs,
            )
        except Exception as e:
            if should_log:
                logger.exception("[MEM0_DEBUG_LLM] exception provider=%s model=%s ctx=%s err=%s", self.provider, self.model, _safe_json(ctx_safe), str(e))
            raise

        if should_log:
            logger.warning(
                "[MEM0_DEBUG_LLM] response provider=%s model=%s ctx=%s raw=%s",
                self.provider,
                self.model,
                _safe_json(ctx_safe),
                _safe_truncate(_safe_json(resp), max_chars),
            )

        return resp


