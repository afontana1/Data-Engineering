#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Context Expansion Techniques: From Prompts to Layered Context
=============================================================

This guide presents hands-on strategies for evolving basic prompts into layered, information-rich
contexts that enhance LLM performance. The focus is on practical context engineering: how to
strategically add and structure context layers, and systematically measure the effects on both
token usage and output quality.

Key concepts covered:
1. Transforming minimal prompts into expanded, context-rich structures
2. Principles of context layering and compositional prompt engineering
3. Quantitative measurement of token usage as context grows
4. Qualitative assessment of model output improvements
5. Iterative approaches to context refinement and optimization

Usage:
    python 02_expand_context.py

Notes:
    - Each section is modular: experiment by editing and running different context layers.
    - Track how additional context alters both cost (token count) and performance (output quality).
    - This file is intentionally a .py script (not a notebook). All narrative is preserved as
      comments/docstrings so the file compiles and can run end-to-end.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple

# Optional dependencies. Keep imports resilient so the file runs even if some are missing.
try:
    import dotenv  # type: ignore
except Exception:
    dotenv = None  # type: ignore

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:
    plt = None  # type: ignore

try:
    import tiktoken  # type: ignore
except Exception:
    tiktoken = None  # type: ignore


# --------------------------------------------------------------------------------------
# Setup and Prerequisites
# --------------------------------------------------------------------------------------
# This guide supports OpenAI and Groq via an OpenAI-compatible client.
#
# Environment variables (choose one):
#   - OPENAI_API_KEY=...
#   - GROQ_API_KEY=...
#
# Optional:
#   - LLM_PROVIDER=openai | groq   (default: auto-detect)
#   - LLM_MODEL=...                (default: provider-specific)
#
# Groq uses an OpenAI-compatible API base URL:
#   https://api.groq.com/openai/v1
# --------------------------------------------------------------------------------------

if dotenv is not None:
    dotenv.load_dotenv()

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

LLM_PROVIDER = (os.getenv("LLM_PROVIDER") or "").strip().lower()
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
GROQ_API_KEY = (os.getenv("GROQ_API_KEY") or "").strip()
LLM_MODEL = (os.getenv("LLM_MODEL") or "").strip()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def _select_provider_and_model() -> Tuple[str, str]:
    """
    Decide provider/model without forcing the user to edit code.
    Priority:
      1) explicit LLM_PROVIDER + LLM_MODEL
      2) explicit LLM_PROVIDER with default model
      3) auto-detect key presence: OpenAI > Groq
    """
    if LLM_PROVIDER in {"openai", "groq"}:
        if LLM_MODEL:
            return LLM_PROVIDER, LLM_MODEL
        return LLM_PROVIDER, (DEFAULT_OPENAI_MODEL if LLM_PROVIDER == "openai" else DEFAULT_GROQ_MODEL)

    # auto-detect
    if OPENAI_API_KEY:
        return "openai", (LLM_MODEL or DEFAULT_OPENAI_MODEL)
    if GROQ_API_KEY:
        return "groq", (LLM_MODEL or DEFAULT_GROQ_MODEL)

    # no keys found
    return "none", (LLM_MODEL or DEFAULT_OPENAI_MODEL)


PROVIDER, MODEL = _select_provider_and_model()


def _build_client() -> Optional[Any]:
    """
    Build an OpenAI-compatible client.
    Uses openai>=1.x SDK if installed.
    """
    if PROVIDER == "none":
        return None

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    if PROVIDER == "openai":
        return OpenAI(api_key=OPENAI_API_KEY)

    # PROVIDER == "groq"
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


CLIENT = _build_client()


def _build_tokenizer(model_name: str) -> Optional[Any]:
    """
    Token counting is best-effort.
    - If tiktoken is unavailable, fallback to a rough heuristic.
    - If model is unknown to tiktoken, fallback to cl100k_base when available.
    """
    if tiktoken is None:
        return None
    try:
        return tiktoken.encoding_for_model(model_name)
    except Exception:
        try:
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None


TOKENIZER = _build_tokenizer(MODEL)


def count_tokens(text: str) -> int:
    """Count tokens in a string using the available tokenizer (best-effort)."""
    if TOKENIZER is not None:
        try:
            return len(TOKENIZER.encode(text))
        except Exception:
            pass
    # Fallback approximation (intentionally simple)
    return int(len(text.split()) * 1.3)


def measure_latency(func, *args, **kwargs) -> Tuple[Any, float]:
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time


# --------------------------------------------------------------------------------------
# 1. Understanding Context Expansion
# --------------------------------------------------------------------------------------
# In the previous guide (01_min_prompt), we explored the basics of atomic prompts.
# Now we'll see how to strategically expand these atoms into molecules (richer context structures).
# We'll measure:
#   - prompt tokens
#   - response tokens
#   - token efficiency (response/prompt)
#   - latency
#   - latency per 1k prompt tokens
# --------------------------------------------------------------------------------------


def calculate_metrics(prompt: str, response: str, latency: float) -> Dict[str, float]:
    """Calculate key metrics for a prompt-response pair."""
    prompt_tokens = count_tokens(prompt)
    response_tokens = count_tokens(response)

    token_efficiency = response_tokens / prompt_tokens if prompt_tokens > 0 else 0.0
    latency_per_1k = (latency / prompt_tokens) * 1000 if prompt_tokens > 0 else 0.0

    return {
        "prompt_tokens": float(prompt_tokens),
        "response_tokens": float(response_tokens),
        "token_efficiency": float(token_efficiency),
        "latency": float(latency),
        "latency_per_1k": float(latency_per_1k),
    }


def generate_response(prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Tuple[str, float]:
    """
    Generate a response from the LLM and measure latency.

    If no client/provider is configured, returns a deterministic placeholder response
    so the rest of the guide can still run (metrics/plots).
    """
    if CLIENT is None:
        placeholder = (
            "LLM is not configured (missing client or API key). "
            "Set OPENAI_API_KEY or GROQ_API_KEY to generate real outputs."
        )
        return placeholder, 0.0

    def _call() -> str:
        resp = CLIENT.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    response_text, latency = measure_latency(_call)
    return response_text, latency


# --------------------------------------------------------------------------------------
# 2. Experiment: Context Expansion Techniques
# --------------------------------------------------------------------------------------
# We'll test different ways to expand a base prompt:
#   - role assignment
#   - few-shot examples
#   - constraints
#   - audience specification
#   - comprehensive (combining multiple layers)
# --------------------------------------------------------------------------------------


def run_experiments() -> Tuple[Dict[str, Dict[str, float]], Dict[str, str], Dict[str, str]]:
    # Base prompt (atom)
    base_prompt = "Write a paragraph about climate change."

    # Expanded prompt variations (molecules)
    expanded_prompts: Dict[str, str] = {
        "base": base_prompt,
        "with_role": (
            "You are an environmental scientist with expertise in climate systems.\n"
            "Write a paragraph about climate change."
        ),
        "with_examples": (
            "Write a paragraph about climate change.\n\n"
            "Example 1:\n"
            "Climate change refers to long-term shifts in temperatures and weather patterns. "
            "Human activities have been the main driver of climate change since the 1800s, "
            "primarily due to the burning of fossil fuels like coal, oil, and gas, which produces "
            "heat-trapping gases.\n\n"
            "Example 2:\n"
            "Global climate change is evident in the increasing frequency of extreme weather events, "
            "rising sea levels, and shifting wildlife populations. Scientific consensus points to "
            "human activity as the primary cause."
        ),
        "with_constraints": (
            "Write a paragraph about climate change.\n"
            "- Include at least one scientific fact with numbers\n"
            "- Mention both causes and effects\n"
            "- End with a call to action\n"
            "- Keep the tone informative but accessible"
        ),
        "with_audience": (
            "Write a paragraph about climate change for high school students who are\n"
            "just beginning to learn about environmental science. Use clear explanations\n"
            "and relatable examples."
        ),
        "comprehensive": (
            "You are an environmental scientist with expertise in climate systems.\n\n"
            "Write a paragraph about climate change for high school students who are\n"
            "just beginning to learn about environmental science. Use clear explanations\n"
            "and relatable examples.\n\n"
            "Guidelines:\n"
            "- Include at least one scientific fact with numbers\n"
            "- Mention both causes and effects\n"
            "- End with a call to action\n"
            "- Keep the tone informative but accessible\n\n"
            "Example of tone and structure:\n"
            "\"Ocean acidification occurs when seawater absorbs CO2 from the atmosphere, causing pH levels to drop. "
            "Since the Industrial Revolution, ocean pH has decreased by 0.1 units, representing a 30% increase in acidity. "
            "This affects marine life, particularly shellfish and coral reefs, as it impairs their ability to form shells and skeletons. "
            "Scientists predict that if emissions continue at current rates, ocean acidity could increase by 150% by 2100, devastating marine ecosystems. "
            "By reducing our carbon footprint through simple actions like using public transportation, we can help protect these vital ocean habitats.\""
        ),
    }

    results: Dict[str, Dict[str, float]] = {}
    responses: Dict[str, str] = {}

    print(f"\nModel: {MODEL}")
    print("Running context expansion experiments...\n")

    for name, prompt in expanded_prompts.items():
        print(f"--- Testing: {name} ---")
        response, latency = generate_response(prompt)
        responses[name] = response
        metrics = calculate_metrics(prompt, response, latency)
        results[name] = metrics
        print(f"Prompt tokens:    {int(metrics['prompt_tokens'])}")
        print(f"Response tokens:  {int(metrics['response_tokens'])}")
        print(f"Latency:         {metrics['latency']:.2f}s")
        print("-" * 40)

    return results, responses, expanded_prompts


# --------------------------------------------------------------------------------------
# 3. Visualizing and Analyzing Results
# --------------------------------------------------------------------------------------
# If matplotlib is installed, we plot:
#   - Token usage (prompt/response)
#   - Token efficiency
#   - Latency
#   - Latency per 1k tokens
# --------------------------------------------------------------------------------------


def plot_results(results: Dict[str, Dict[str, float]]) -> None:
    if plt is None:
        print("\nmatplotlib not installed. Skipping plots.\n")
        return

    prompt_types = list(results.keys())
    prompt_tokens = [results[k]["prompt_tokens"] for k in prompt_types]
    response_tokens = [results[k]["response_tokens"] for k in prompt_types]
    latencies = [results[k]["latency"] for k in prompt_types]
    token_efficiency = [results[k]["token_efficiency"] for k in prompt_types]
    latency_per_1k = [results[k]["latency_per_1k"] for k in prompt_types]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Token usage
    axes[0, 0].bar(prompt_types, prompt_tokens, label="Prompt Tokens", alpha=0.7)
    axes[0, 0].bar(prompt_types, response_tokens, bottom=prompt_tokens, label="Response Tokens", alpha=0.7)
    axes[0, 0].set_title("Token Usage by Prompt Type")
    axes[0, 0].set_ylabel("Tokens")
    axes[0, 0].legend()
    plt.setp(axes[0, 0].get_xticklabels(), rotation=45, ha="right")

    # Token efficiency
    axes[0, 1].bar(prompt_types, token_efficiency, alpha=0.7)
    axes[0, 1].set_title("Token Efficiency (Response/Prompt)")
    axes[0, 1].set_ylabel("Efficiency Ratio")
    plt.setp(axes[0, 1].get_xticklabels(), rotation=45, ha="right")

    # Latency
    axes[1, 0].bar(prompt_types, latencies, alpha=0.7)
    axes[1, 0].set_title("Response Latency")
    axes[1, 0].set_ylabel("Seconds")
    plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha="right")

    # Latency per 1k
    axes[1, 1].bar(prompt_types, latency_per_1k, alpha=0.7)
    axes[1, 1].set_title("Latency per 1k Prompt Tokens")
    axes[1, 1].set_ylabel("Seconds per 1k")
    plt.setp(axes[1, 1].get_xticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------------------------------------------
# 4. Qualitative Analysis
# --------------------------------------------------------------------------------------
# We print the full responses so you can compare output quality across prompts.
# --------------------------------------------------------------------------------------


def print_responses(responses: Dict[str, str]) -> None:
    print("\nQualitative Analysis (Responses)\n" + "=" * 80)
    for name, response in responses.items():
        print(f"\n=== Response for '{name}' prompt ===\n")
        print(response)
        print("\n" + "=" * 80)


# --------------------------------------------------------------------------------------
# 5. Context Expansion Patterns
# --------------------------------------------------------------------------------------
# Based on our experiments, we can identify several effective context expansion patterns:
#   1) Role Assignment
#   2) Few-shot Examples
#   3) Constraint Definition
#   4) Audience Specification
#   5) Comprehensive Context (combining multiple elements)
# --------------------------------------------------------------------------------------


def create_expanded_context(
    base_prompt: str,
    role: Optional[str] = None,
    examples: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    output_format: Optional[str] = None,
) -> str:
    """
    Create an expanded context from a base prompt with optional components.

    Args:
        base_prompt: The core instruction or question
        role: Who the model should act as
        examples: List of example outputs to guide the model
        constraints: List of requirements or boundaries
        audience: Who the output is intended for
        tone: Desired tone of the response
        output_format: Specific format requirements

    Returns:
        Expanded context as a string
    """
    context_parts: List[str] = []

    if role:
        context_parts.append(f"You are {role}.")

    context_parts.append(base_prompt)

    if audience:
        context_parts.append(f"Your response should be suitable for {audience}.")

    if tone:
        context_parts.append(f"Use a {tone} tone in your response.")

    if output_format:
        context_parts.append(f"Format your response as {output_format}.")

    if constraints:
        context_parts.append("Requirements:")
        for c in constraints:
            context_parts.append(f"- {c}")

    if examples:
        context_parts.append("Examples:")
        for i, ex in enumerate(examples, 1):
            context_parts.append(f"Example {i}:\n{ex}")

    return "\n\n".join(context_parts)


def demo_template() -> None:
    new_base_prompt = "Explain how photosynthesis works."

    new_expanded_context = create_expanded_context(
        base_prompt=new_base_prompt,
        role="a biology teacher with 15 years of experience",
        audience="middle school students",
        tone="enthusiastic and educational",
        constraints=[
            "Use a plant-to-factory analogy",
            "Mention the role of chlorophyll",
            "Explain the importance for Earth's ecosystem",
            "Keep it under 200 words",
        ],
        examples=[
            (
                "Photosynthesis is like a tiny factory inside plants. Just as a factory needs raw materials, "
                "energy, and workers to make products, plants need carbon dioxide, water, sunlight, and "
                "chlorophyll to make glucose (sugar) and oxygen. The sunlight is the energy source, "
                "chlorophyll molecules are the workers that capture this energy, while carbon dioxide and "
                "water are the raw materials. The factory's products are glucose, which the plant uses for "
                "growth and energy storage, and oxygen, which is released into the air for animals like us "
                "to breathe. This process is essential for life on Earth because it provides the oxygen we "
                "need and removes carbon dioxide from the atmosphere."
            )
        ],
    )

    print("\nTemplate-generated expanded context:\n" + "-" * 80)
    print(new_expanded_context)
    print("-" * 80)
    print(f"Token count (best-effort): {count_tokens(new_expanded_context)}")

    response, latency = generate_response(new_expanded_context)
    metrics = calculate_metrics(new_expanded_context, response, latency)

    print("\nResponse:\n" + "-" * 80)
    print(response)
    print("-" * 80)
    print(f"Response tokens (best-effort): {int(metrics['response_tokens'])}")
    print(f"Latency: {metrics['latency']:.2f}s")


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------


def main() -> None:
    if PROVIDER == "none":
        print(
            "No LLM provider configured.\n"
            "Set OPENAI_API_KEY or GROQ_API_KEY (or set LLM_PROVIDER=openai|groq).\n"
            "This script will still run with placeholder responses.\n"
        )
    else:
        if CLIENT is None:
            print(
                "Provider was selected but the OpenAI-compatible SDK client could not be created.\n"
                "Install the OpenAI Python SDK: pip install openai\n"
                "Then re-run.\n"
            )

    results, responses, _prompts = run_experiments()
    plot_results(results)
    print_responses(responses)
    demo_template()


if __name__ == "__main__":
    main()
