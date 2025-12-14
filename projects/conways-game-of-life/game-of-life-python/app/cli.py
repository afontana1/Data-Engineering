"""CLI entrypoint to run the Game of Life FastAPI server."""
from __future__ import annotations

import argparse
import sys

import uvicorn


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="game-of-life",
        description="Start the Game of Life streaming FastAPI server.",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable reload (for development).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (ignored if --reload).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=None if args.reload else args.workers,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
