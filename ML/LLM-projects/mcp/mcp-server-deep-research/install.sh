#!/bin/bash
# Install script for the MCP server deep research package

echo "Finding the latest wheel file..."
WHEEL_FILE=$(ls -t /Users/hezhang/repos/mcp-server-application/mcp-server-deep-research/dist/*.whl | head -1)

if [ -z "$WHEEL_FILE" ]; then
  echo "No wheel file found. Please run build.sh first."
  exit 1
fi

echo "Installing wheel file: $WHEEL_FILE"
uv pip install --force-reinstall $WHEEL_FILE

echo "Creating/updating Claude desktop config..."
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create or update config file
if [ -f "$CONFIG_FILE" ]; then
  # Update existing config
  echo "Updating existing Claude config..."
  
  # Check if jq is installed
  if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Creating a new config file..."
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "mcp-server-deep-research": {
      "command": "mcp-server-deep-research"
    }
  }
}
EOF
  else
    # Use jq to update config
    jq '.mcpServers."mcp-server-deep-research" = {"command": "mcp-server-deep-research"}' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
  fi
else
  # Create new config file
  echo "Creating new Claude config file..."
  cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "mcp-server-deep-research": {
      "command": "mcp-server-deep-research"
    }
  }
}
EOF
fi

echo "Installation complete. Restart Claude to use the updated server."
