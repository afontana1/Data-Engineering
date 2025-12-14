from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from app.life.engine import run_simulation
from app.life.patterns import get_pattern, list_patterns
from app.life.schemas import GenerationState, SimulationConfig

app = FastAPI(title="Game of Life Streaming API", version="0.1.0")


@app.get("/patterns")
async def available_patterns():
    return {"patterns": list(list_patterns())}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/simulate")
async def websocket_simulation(ws: WebSocket):
    await ws.accept()
    try:
        initial: Dict[str, Any] = await ws.receive_json()
        config = SimulationConfig(**initial)
    except Exception as exc:  # noqa: BLE001 - report to client
        await ws.send_json({"error": f"Invalid configuration: {exc}"})
        await ws.close()
        return

    try:
        pattern = get_pattern(
            name=config.pattern, random_fill=config.random_fill, size_hint=min(config.width, config.height)
        )
    except Exception as exc:  # noqa: BLE001
        await ws.send_json({"error": str(exc)})
        await ws.close()
        return

    try:
        async for state in run_simulation(config=config, pattern=pattern):
            await ws.send_json(state.model_dump())
    except WebSocketDisconnect:
        return
    except Exception as exc:  # noqa: BLE001
        await ws.send_json({"error": f"Simulation error: {exc}"})
        await ws.close()


@app.get("/")
async def index():
    return JSONResponse(
        {
            "message": "Use /patterns to list patterns and /ws/simulate WebSocket to stream generations."
        }
    )
