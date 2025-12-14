# telemetry/litellm_instrumentation.py
from __future__ import annotations

import time
import uuid
import asyncio
from typing import Any, Callable, Awaitable, Optional

import litellm
from litellm import token_counter  # model-aware, falls back to tiktoken :contentReference[oaicite:4]{index=4}

from token_tracker.telemetry.context import usage_ctx_var
from token_tracker.telemetry.sink import UsageSink


def _now_ms() -> int:
    return int(time.time() * 1000)


def _extract_text_from_nonstream_response(resp: Any) -> str:
    """
    LiteLLM follows OpenAI-style output formats for completions. :contentReference[oaicite:5]{index=5}
    Best-effort extraction.
    """
    # ChatCompletions-ish: resp.choices[0].message.content
    try:
        choices = resp.get("choices") if isinstance(resp, dict) else getattr(resp, "choices", None)
        if not choices:
            return ""
        c0 = choices[0]
        msg = c0.get("message") if isinstance(c0, dict) else getattr(c0, "message", None)
        if not msg:
            return ""
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
        return content or ""
    except Exception:
        return ""


def _extract_text_delta_from_stream_chunk(chunk: Any) -> str:
    """
    Best-effort extraction of streamed delta text.
    Typical shape: chunk.choices[0].delta.content
    """
    try:
        choices = chunk.get("choices") if isinstance(chunk, dict) else getattr(chunk, "choices", None)
        if not choices:
            return ""
        c0 = choices[0]
        delta = c0.get("delta") if isinstance(c0, dict) else getattr(c0, "delta", None)
        if not delta:
            return ""
        content = delta.get("content") if isinstance(delta, dict) else getattr(delta, "content", "")
        return content or ""
    except Exception:
        return ""


def _count_prompt_tokens(model: str, kwargs: dict) -> int:
    # LiteLLM token_counter supports messages; uses model tokenizer and falls back as needed :contentReference[oaicite:6]{index=6}
    if "messages" in kwargs and kwargs["messages"] is not None:
        return int(token_counter(model=model, messages=kwargs["messages"]))
    if "input" in kwargs and kwargs["input"] is not None:
        # responses API sometimes uses `input`
        return int(token_counter(model=model, text=str(kwargs["input"])))
    if "prompt" in kwargs and kwargs["prompt"] is not None:
        return int(token_counter(model=model, text=str(kwargs["prompt"])))
    return 0


class LiteLLMInstrumentation:
    def __init__(self, sink: UsageSink):
        self.sink = sink
        self._orig_acompletion = None
        self._orig_aresponses = None

    def install(self) -> None:
        # Save originals
        self._orig_acompletion = getattr(litellm, "acompletion", None)
        self._orig_aresponses = getattr(litellm, "aresponses", None)

        if self._orig_acompletion:
            litellm.acompletion = self._wrap_async_fn(self._orig_acompletion, kind="acompletion")

        if self._orig_aresponses:
            litellm.aresponses = self._wrap_async_fn(self._orig_aresponses, kind="aresponses")

    def uninstall(self) -> None:
        if self._orig_acompletion:
            litellm.acompletion = self._orig_acompletion
        if self._orig_aresponses:
            litellm.aresponses = self._orig_aresponses

    def _wrap_async_fn(self, fn: Callable[..., Awaitable[Any]], *, kind: str):
        async def wrapped(*args, **kwargs):
            ctx = usage_ctx_var.get()
            call_id = str(uuid.uuid4())
            started_ms = _now_ms()
            model = kwargs.get("model", "unknown")

            prompt_tokens = 0
            try:
                prompt_tokens = _count_prompt_tokens(model, kwargs)
            except Exception:
                # token_counter can fail for unknown models; treat as 0 rather than breaking calls
                prompt_tokens = 0

            try:
                # Call underlying LiteLLM
                resp = await fn(*args, **kwargs)

                # Handle streaming
                if kwargs.get("stream") is True:
                    # resp is an async iterator (LiteLLM supports async streaming) :contentReference[oaicite:7]{index=7}
                    return self._wrap_stream(
                        resp,
                        kind=kind,
                        model=model,
                        prompt_tokens=prompt_tokens,
                        ctx=ctx,
                        call_id=call_id,
                        started_ms=started_ms,
                    )

                # Non-streaming: count from returned text (do NOT rely on resp.usage)
                text = _extract_text_from_nonstream_response(resp)
                completion_tokens = 0
                try:
                    completion_tokens = int(token_counter(model=model, text=text))
                except Exception:
                    completion_tokens = 0

                await self.sink.write({
                    "ts_ms": started_ms,
                    "latency_ms": _now_ms() - started_ms,
                    "kind": kind,
                    "call_id": call_id,
                    "model": model,
                    "prompt_tokens_est": prompt_tokens,
                    "completion_tokens_est": completion_tokens,
                    "total_tokens_est": prompt_tokens + completion_tokens,
                    "user_id": getattr(ctx, "user_id", None) if ctx else None,
                    "org_id": getattr(ctx, "org_id", None) if ctx else None,
                    "session_id": getattr(ctx, "session_id", None) if ctx else None,
                    "trace_id": getattr(ctx, "trace_id", None) if ctx else None,
                    "status": "ok",
                })
                return resp

            except Exception as e:
                await self.sink.write({
                    "ts_ms": started_ms,
                    "latency_ms": _now_ms() - started_ms,
                    "kind": kind,
                    "call_id": call_id,
                    "model": model,
                    "prompt_tokens_est": prompt_tokens,
                    "completion_tokens_est": None,
                    "total_tokens_est": None,
                    "user_id": getattr(ctx, "user_id", None) if ctx else None,
                    "org_id": getattr(ctx, "org_id", None) if ctx else None,
                    "session_id": getattr(ctx, "session_id", None) if ctx else None,
                    "trace_id": getattr(ctx, "trace_id", None) if ctx else None,
                    "status": "error",
                    "error_type": type(e).__name__,
                    "error": str(e),
                })
                raise

        return wrapped

    def _wrap_stream(self, stream_obj: Any, *, kind: str, model: str, prompt_tokens: int,
                     ctx: Any, call_id: str, started_ms: int):
        async def gen():
            parts: list[str] = []
            try:
                async for chunk in stream_obj:
                    delta = _extract_text_delta_from_stream_chunk(chunk)
                    if delta:
                        parts.append(delta)
                    yield chunk
            finally:
                # finalize metrics even if consumer breaks early
                text = "".join(parts)
                try:
                    completion_tokens = int(token_counter(model=model, text=text))
                except Exception:
                    completion_tokens = 0

                await self.sink.write({
                    "ts_ms": started_ms,
                    "latency_ms": _now_ms() - started_ms,
                    "kind": kind,
                    "call_id": call_id,
                    "model": model,
                    "prompt_tokens_est": prompt_tokens,
                    "completion_tokens_est": completion_tokens,
                    "total_tokens_est": prompt_tokens + completion_tokens,
                    "user_id": getattr(ctx, "user_id", None) if ctx else None,
                    "org_id": getattr(ctx, "org_id", None) if ctx else None,
                    "session_id": getattr(ctx, "session_id", None) if ctx else None,
                    "trace_id": getattr(ctx, "trace_id", None) if ctx else None,
                    "status": "ok_stream",
                })

        return gen()
