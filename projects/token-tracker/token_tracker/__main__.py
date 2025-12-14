"""
CLI entrypoint for token_tracker.

Runs the FastAPI app via uvicorn. Customize host/port with:
  TOKEN_TRACKER_HOST, TOKEN_TRACKER_PORT, TOKEN_TRACKER_RELOAD
"""

import os

import uvicorn


def main() -> None:
    host = os.getenv("TOKEN_TRACKER_HOST", "0.0.0.0")
    port = int(os.getenv("TOKEN_TRACKER_PORT", "8000"))
    reload = os.getenv("TOKEN_TRACKER_RELOAD", "false").lower() in {"1", "true", "yes", "on"}
    uvicorn.run("token_tracker.app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
