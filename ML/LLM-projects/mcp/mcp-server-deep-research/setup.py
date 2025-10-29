#!/usr/bin/env python3
"""Setup script for MCP server deep research environment."""

import json
import subprocess
import sys
from pathlib import Path
import re
import time


def run_command(cmd, check=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        return None


def ask_permission(question):
    """Ask user for permission."""
    while True:
        response = input(f"{question} (y/n): ").lower()
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please answer 'y' or 'n'")


def check_uv():
    """Check if uv is installed and install if needed."""
    if not run_command("which uv", check=False):
        if ask_permission("uv is not installed. Would you like to install it?"):
            print("Installing uv...")
            run_command("curl -LsSf https://astral.sh/uv/install.sh | sh")
            print("uv installed successfully")
        else:
            sys.exit("uv is required to continue")


def setup_venv():
    """Create virtual environment if it doesn't exist."""
    if not Path(".venv").exists():
        if ask_permission("Virtual environment not found. Create one?"):
            print("Creating virtual environment...")
            run_command("uv venv")
            print("Virtual environment created successfully")
        else:
            sys.exit("Virtual environment is required to continue")


def sync_dependencies():
    """Sync project dependencies."""
    print("Syncing dependencies...")
    run_command("uv sync")
    print("Dependencies synced successfully")


def check_claude_desktop():
    """Check if Claude desktop app is installed."""
    app_path = "/Applications/Claude.app"
    if not Path(app_path).exists():
        print("Claude desktop app not found.")
        print("Please download and install from: https://claude.ai/download")
        if not ask_permission("Continue after installing Claude?"):
            sys.exit("Claude desktop app is required to continue")


def setup_claude_config():
    """Setup Claude desktop config file."""
    config_path = Path(
        "~/Library/Application Support/Claude/claude_desktop_config.json"
    ).expanduser()
    config_dir = config_path.parent

    if not config_dir.exists():
        config_dir.mkdir(parents=True)

    config = (
        {"mcpServers": {}}
        if not config_path.exists()
        else json.loads(config_path.read_text())
    )
    return config_path, config


def build_package():
    """Build package and get wheel path."""
    print("Building package...")
    try:
        # Use Popen for real-time and complete output capture
        process = subprocess.Popen(
            "uv build",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()  # Capture output
        output = stdout + stderr  # Combine both streams
        print(f"Raw output: {output}")  # Debug: check output
    except Exception as e:
        sys.exit(f"Error running build: {str(e)}")

    # Check if the command was successful
    if process.returncode != 0:
        sys.exit(f"Build failed with error code {process.returncode}")

    # Extract wheel file path from the combined output
    match = re.findall(r"dist/[^\s]+\.whl", output.strip())
    whl_file = match[-1] if match else None
    if not whl_file:
        sys.exit("Failed to find wheel file in build output")

    # Convert to absolute path
    path = Path(whl_file).absolute()
    return str(path)


def update_config(config_path, config, wheel_path):
    """Update Claude config with MCP server settings."""
    config.setdefault("mcpServers", {})
    config["mcpServers"]["mcp-server-deep-research"] = {
        "command": "uvx",
        "args": ["--from", wheel_path, "mcp-server-deep-research"],
    }

    config_path.write_text(json.dumps(config, indent=2))
    print(f"Updated config at {config_path}")


def restart_claude():
    """Restart Claude desktop app if running."""
    if run_command("pgrep -x Claude", check=False):
        if ask_permission("Claude is running. Restart it?"):
            print("Restarting Claude...")
            run_command("pkill -x Claude")
            time.sleep(2)
            run_command("open -a Claude")
            print("Claude restarted successfully")
    else:
        print("Starting Claude...")
        run_command("open -a Claude")


def main():
    """Main setup function."""
    print("Starting setup...")
    check_uv()
    setup_venv()
    sync_dependencies()
    check_claude_desktop()
    config_path, config = setup_claude_config()
    wheel_path = build_package()
    update_config(config_path, config, wheel_path)
    restart_claude()
    print("Setup completed successfully!")


if __name__ == "__main__":
    main()
