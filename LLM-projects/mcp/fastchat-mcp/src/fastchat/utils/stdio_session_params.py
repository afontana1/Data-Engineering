import os
from mcp import StdioServerParameters
import shutil


def get_stdio_session_params(server) -> StdioServerParameters:
    config: dict = server["config"]

    server_params: StdioServerParameters = StdioServerParameters(
        command=(
            shutil.which("npx") if config["command"] == "npx" else config["command"]
        ),
        args=config["args"],
        env={**os.environ, **config["env"]} if config.get("env") else None,
    )
    return server_params
