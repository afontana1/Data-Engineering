"""
MCP server providing access to arXiv papers through their API.
"""
import asyncio
from .server import main as server_main

__version__ = "0.1.0"

def main():
    """Main entry point for the package."""
    asyncio.run(server_main())