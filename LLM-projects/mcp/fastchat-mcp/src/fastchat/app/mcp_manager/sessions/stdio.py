import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import shutil
from ....config.logger import logging
from ....utils.stdio_session_params import get_stdio_session_params

# CLEANUP IMPLEMENTATION CHANGE:
# Global dictionary to store active stdio sessions for proper cleanup
# This allows us to track and terminate subprocess connections later
_active_sessions: dict[str, tuple] = {}


def get_session_data(server: dict) -> dict:
    try:
        loop = asyncio.get_running_loop()
        task = loop.create_task(async_get_session(server=server))
        return asyncio.run_coroutine_threadsafe(async_get_session(server=server), loop).result()
    except RuntimeError:
        return asyncio.run(async_get_session(server=server))


async def async_get_session(server: dict) -> dict:
    """Initialize the server connection."""
    name: str = server["name"]
    server_params: StdioServerParameters = get_stdio_session_params(server=server)

    # CLEANUP IMPLEMENTATION CHANGE:
    # Generate session key for tracking active subprocess connections
    session_key = f"{name}_{id(server_params)}"

    try:
        # CLEANUP IMPLEMENTATION CHANGE:
        # Instead of using context managers that close immediately,
        # manually manage the connection lifecycle for later cleanup
        connection = stdio_client(server_params)
        read, write = await connection.__aenter__()
        
        # Create session
        session = ClientSession(read, write)
        await session.__aenter__()
        
        # CLEANUP IMPLEMENTATION CHANGE:
        # Store active session references for cleanup tracking
        # This allows close_session() to properly terminate subprocesses
        _active_sessions[session_key] = (connection, session, server_params)
        
        await session.initialize()
        tools = await session.list_tools()
        resources = await session.list_resource_templates()
        prompts = await session.list_prompts()
        data: dict = {
            "tools": tools.tools,
            "resources": resources.resourceTemplates,
            "prompts": prompts.prompts,
            "_session_key": session_key,  # Include key for cleanup tracking
        }
        return data

    except Exception as e:
        # If error, cleanup immediately to prevent resource leaks
        await close_session_by_key(session_key)
        logging.error(f"Error initializing server {name}: {e}")
        raise Exception(f"Error initializing server {name}: {e}")


async def close_session(server: dict) -> None:
    """
    Close stdio session for the given server.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function closes subprocess connections for a specific MCP server.
    It reconstructs the session key from server configuration and calls
    close_session_by_key to perform the actual cleanup.
    
    Args:
        server (dict): Server configuration containing connection details
    """
    # Reconstruct session key from server config
    name: str = server["name"]
    server_params: StdioServerParameters = get_stdio_session_params(server=server)
    session_key = f"{name}_{id(server_params)}"
    
    await close_session_by_key(session_key)


async def close_session_by_key(session_key: str) -> None:
    """
    Close session by its key.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function performs the actual cleanup of subprocess connections.
    It properly closes the session and connection using their __aexit__ methods
    and removes the session from the active sessions dictionary.
    
    Args:
        session_key (str): The session key to close
    """
    if session_key in _active_sessions:
        connection, session, server_params = _active_sessions[session_key]
        
        try:
            # Close session properly using context manager protocol
            await session.__aexit__(None, None, None)
        except Exception:
            pass  # Ignore cleanup errors
        
        try:
            # Close stdio connection (this should terminate the subprocess)
            await connection.__aexit__(None, None, None)
        except Exception:
            pass  # Ignore cleanup errors
        
        # Remove from active sessions tracking
        del _active_sessions[session_key]


async def close_all_sessions() -> None:
    """
    Close all active stdio sessions.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function closes all currently active subprocess sessions.
    Useful for complete cleanup when shutting down the application.
    """
    session_keys = list(_active_sessions.keys())
    for session_key in session_keys:
        await close_session_by_key(session_key)
