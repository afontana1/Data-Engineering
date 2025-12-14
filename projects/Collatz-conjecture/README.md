# Collatz Conjecture API

FastAPI service and reusable Python package for computing Collatz (3n + 1) sequences.

## Quickstart

```bash
pip install -e .[test]
collatz --reload --port 8000
```

Open Swagger UI at http://127.0.0.1:8000/docs.

## Endpoints

- `GET /health` — basic health check.
- `POST /collatz/sequence` — body: `{ "start": <positive int>, "max_steps": <optional positive int> }`; returns full sequence, iterations, and whether it reached 1.
- `POST /collatz/scan` — body: `{ "start": <positive int>, "count": <positive int>, "max_steps": <optional positive int> }`; returns metadata for a range of starting numbers (no graph files are written).

## Library usage

```python
from collatz.core import collatz_sequence, collatz_scan_range

result = collatz_sequence(7)
print(result.sequence)      # [7, 22, 11, 34, ... , 1]
print(result.iterations)    # 16

scan = collatz_scan_range(start=1, count=3)
```

## Testing

```bash
pip install -e .[test]
pytest
```

## Frontend (static)

A minimal HTML/CSS/JS frontend lives in `frontend/`.

Serve it with any static server, e.g.:
```bash
python -m http.server 8080 --directory frontend
```
Then open http://localhost:8080 and point the API URL input to your running backend (default `http://localhost:8000`).
