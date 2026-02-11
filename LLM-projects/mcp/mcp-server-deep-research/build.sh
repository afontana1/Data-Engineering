#!/bin/bash
# Build script for the MCP server deep research package

echo "Building mcp-server-deep-research package..."
cd /Users/hezhang/repos/mcp-server-application/mcp-server-deep-research
uv build

echo "Done building. The wheel file should be in the dist/ directory."
ls -la dist/
