import argparse
from typing import Optional

import uvicorn


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Collatz FastAPI server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind.")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable autoreload (useful for local development).",
    )
    args = parser.parse_args(argv)

    uvicorn.run(
        "collatz.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=False,
    )


if __name__ == "__main__":
    main()
