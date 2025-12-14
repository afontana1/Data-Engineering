# token_tracker/routes/chat.py
from __future__ import annotations

import asyncio
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Request, Query
from pydantic import BaseModel, Field

# ---- Optional .env loading (recommended for local dev) ----
# LiteLLM reads OPENAI_API_KEY from environment variables.
# If you don't want python-dotenv, remove this block and set env vars another way.
try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except Exception:
    pass

import litellm

# If you already have request-context identity in middleware + ContextVar, importing it here
# lets us return trace_id in responses (optional).
try:
    from token_tracker.telemetry.context import usage_ctx_var  # your telemetry package
except Exception:
    usage_ctx_var = None  # telemetry still works via global wrapper, this is only for response metadata


router = APIRouter()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))


# -----------------------------
# Fake "tools" (no external deps)
# -----------------------------
def fake_rag_lookup(question: str) -> List[Dict[str, Any]]:
    """Pretend we called an external RAG service and got documents back."""
    return [
        {"id": "doc_1", "title": "Internal Policy", "text": "All expenses must be tagged by org_id and user_id."},
        {"id": "doc_2", "title": "Architecture Notes", "text": "Multi-agent flows may trigger N LLM calls per request."},
        {"id": "doc_3", "title": "FAQ", "text": f"Question observed: {question[:80]}"},
    ]


def fake_db_execute(sql: str) -> List[Dict[str, Any]]:
    """Pretend we executed SQL and got rows back."""
    return [
        {"month": "2025-10", "spend_usd": 1234.56},
        {"month": "2025-11", "spend_usd": 1678.90},
        {"month": "2025-12", "spend_usd": 2222.22},
        {"_sql_used": sql},
    ]


# -----------------------------
# LLM helper
# -----------------------------
async def llm_chat(messages: List[Dict[str, Any]], *, model: str = MODEL, temperature: float = TEMPERATURE) -> str:
    """
    Single place to call LiteLLM in this module.
    If you installed global LiteLLM instrumentation in app startup,
    you do NOT need to modify this function for telemetry to work.
    """
    resp = await litellm.acompletion(model=model, messages=messages, temperature=temperature)
    # LiteLLM usually returns OpenAI-style shapes. Extract best-effort:
    try:
        return resp["choices"][0]["message"]["content"] or ""
    except Exception:
        return ""


def _extract_json_array(text: str) -> List[str]:
    """
    Robustly parse a JSON array from model output.
    Accepts either a raw JSON array or JSON embedded in text.
    """
    if not text:
        return []
    # Try direct parse
    try:
        obj = json.loads(text)
        if isinstance(obj, list) and all(isinstance(x, str) for x in obj):
            return obj
    except Exception:
        pass

    # Try to find the first JSON array substring
    m = re.search(r"\[[\s\S]*\]", text)
    if not m:
        return []
    try:
        obj = json.loads(m.group(0))
        if isinstance(obj, list):
            return [str(x) for x in obj]
    except Exception:
        return []
    return []


# -----------------------------
# Agents (fake but LLM-backed)
# -----------------------------
async def graph_agent(question: str) -> List[Dict[str, Any]]:
    """Calls an LLM to generate a 'graph spec'."""
    messages = [
        {"role": "system", "content": "You are a graph agent. Output a compact JSON graph spec."},
        {"role": "user", "content": f"Create a simple graph spec for: {question}"},
    ]
    spec = await llm_chat(messages)
    return [{"agent": "graph-agent", "type": "graph_spec", "content": spec}]


async def rag_agent(question: str) -> List[Dict[str, Any]]:
    """Calls a fake RAG tool then summarizes with LLM."""
    docs = fake_rag_lookup(question)
    doc_text = "\n\n".join([f"- {d['title']}: {d['text']}" for d in docs])
    messages = [
        {"role": "system", "content": "You are a RAG agent. Summarize the provided documents for the user question."},
        {"role": "user", "content": f"Question: {question}\n\nDocs:\n{doc_text}\n\nReturn a short answer."},
    ]
    summary = await llm_chat(messages)
    return [{"agent": "rag-agent", "type": "rag_summary", "content": summary, "docs": [d["id"] for d in docs]}]


async def database_agent(question: str) -> List[Dict[str, Any]]:
    """Generates SQL with LLM, then uses a fake DB tool to return rows."""
    messages = [
        {"role": "system", "content": "You write SQL for a fictional table spend(month, spend_usd). Return SQL only."},
        {"role": "user", "content": f"Write SQL to answer: {question}"},
    ]
    sql = (await llm_chat(messages)).strip()
    rows = fake_db_execute(sql)
    return [{"agent": "data-base-agent", "type": "db_result", "content": rows}]


async def synthesizer_agent(question: str, agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calls LLM to synthesize final response from agent outputs."""
    compact = json.dumps(agent_outputs, ensure_ascii=False)[:12_000]  # keep prompts bounded
    messages = [
        {"role": "system", "content": "You are a synthesizer. Combine agent outputs into a helpful final answer."},
        {"role": "user", "content": f"Question: {question}\n\nAgent outputs JSON:\n{compact}\n\nWrite the final response."},
    ]
    final = await llm_chat(messages, temperature=0.3)
    return {"agent": "synthesizer-agent", "type": "final", "content": final}


AGENTS = {
    "graph-agent": graph_agent,
    "rag-agent": rag_agent,
    "data-base-agent": database_agent,
    # synthesizer-agent is invoked separately (after others)
}


# -----------------------------
# Orchestrator (LLM-based router)
# -----------------------------
async def orchestrator(question: str) -> List[str]:
    """
    Chooses which agents to call. This itself calls the LLM so telemetry sees:
      - router call
      - N agent calls
      - synthesizer call
    """
    allowed = list(AGENTS.keys())
    messages = [
        {"role": "system", "content": "You are a router. Pick relevant agents. Output ONLY a JSON array of strings."},
        {"role": "user", "content": f"Allowed agents: {allowed}\nQuestion: {question}"},
    ]
    text = await llm_chat(messages, temperature=0.0)
    picked = _extract_json_array(text)

    # Safety fallback: choose something sensible if parsing fails
    if not picked:
        picked = ["rag-agent"]
        if any(w in question.lower() for w in ["sql", "database", "query", "spend"]):
            picked.append("data-base-agent")
        if any(w in question.lower() for w in ["chart", "graph", "plot"]):
            picked.append("graph-agent")

    # Filter to known agents, de-dupe, preserve order
    seen = set()
    final = []
    for a in picked:
        if a in AGENTS and a not in seen:
            seen.add(a)
            final.append(a)
    return final


# -----------------------------
# API models + routes
# -----------------------------
class ChatBody(BaseModel):
    question: str = Field(..., min_length=1, max_length=10_000)
    # optional session continuation ID you already manage in your app
    session_id: Optional[str] = None


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/my-chat-bot")
async def chat_get(q: str = Query(..., min_length=1)):
    """
    Simple GET for quick manual testing:
      /my-chat-bot?q=hello
    """
    return await _handle_chat(question=q)


@router.post("/my-chat-bot")
async def chat_post(body: ChatBody, request: Request):
    """
    Proper POST for real usage.
    If your middleware sets user/org/session contextvars, telemetry will attribute calls automatically.
    """
    return await _handle_chat(question=body.question, session_id=body.session_id)


async def _handle_chat(*, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    picked_agents = await orchestrator(question)

    # Run agents concurrently to stress-test context propagation + telemetry across async tasks
    tasks = [AGENTS[name](question) for name in picked_agents]
    agent_results_nested = await asyncio.gather(*tasks)
    agent_outputs: List[Dict[str, Any]] = []
    for lst in agent_results_nested:
        agent_outputs.extend(lst)

    # Synthesize final answer (another LLM call)
    final = await synthesizer_agent(question, agent_outputs)

    # Optional: expose trace_id to help you join API response -> telemetry rows
    trace_id = None
    if usage_ctx_var is not None:
        ctx = usage_ctx_var.get()
        trace_id = getattr(ctx, "trace_id", None) if ctx else None

    return {
        "question": question,
        "picked_agents": picked_agents,
        "agent_outputs": agent_outputs,
        "answer": final["content"],
        "trace_id": trace_id,
        "session_id": session_id,
    }
