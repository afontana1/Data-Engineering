# Game of Life (FastAPI + Streaming)

Stream Conway's Game of Life generations over WebSocket via FastAPI. A CLI entrypoint starts the server.

## Install

```bash
pip install -e .
```
If you see a WebSocket warning from uvicorn, ensure the WebSocket extra is installed:
```bash
pip install -e .  # after pulling updates (includes uvicorn[standard])
# or explicitly:
pip install "uvicorn[standard]" "websockets>=12.0"
```

## Run the server (CLI)

```bash
game-of-life --host 0.0.0.0 --port 8000 --reload
```

Then:
- WebSocket: connect to `ws://localhost:8000/ws/simulate` and send JSON config, e.g.
  ```json
  {"width": 40, "height": 40, "generations": 200, "delay_ms": 150, "pattern": "Glider", "wrap": true}
  ```
  Frames stream back as `{"generation": n, "width": w, "height": h, "alive": [[y,x], ...]}`.
- Patterns: `GET http://localhost:8000/patterns`
- Health: `GET http://localhost:8000/health`

## Config fields
- `width`, `height`: board size (ints > 0)
- `generations`: optional limit; omit for endless
- `delay_ms`: milliseconds between frames
- `pattern`: `"Random"` or named pattern from `/patterns`
- `random_fill`: 0-1 density for random pattern
- `wrap`: `true` for toroidal edges

## Frontend (static)

Run a simple HTTP server for the static UI:

```bash
python frontend/serve.py
# or:
python -m http.server 8080 --directory frontend
```

Then open http://localhost:8080 in your browser. The page connects to the backend WebSocket (defaults to `ws://localhost:8000/ws/simulate`), sends the selected config, and renders the streamed generations on a canvas. Adjust the WS URL in the UI if your backend runs elsewhere.

## Tests

```bash
pytest
```
