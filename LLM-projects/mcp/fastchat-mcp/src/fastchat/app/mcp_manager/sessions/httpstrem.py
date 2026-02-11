from mcp.client.streamable_http import streamablehttp_client
from mcp.client.auth import OAuthClientProvider
from mcp import ClientSession
import asyncio

from mcp_oauth import OAuthClient

# CLEANUP IMPLEMENTATION CHANGE:
# Global dictionary to store active sessions for proper cleanup
# This allows us to track and close HTTP/WebSocket connections later
_active_sessions: dict[str, tuple] = {}


def get_session_data(
    http: str,
    oauth_client: OAuthClient,
    headers: dict[str, str] | None = None,
) -> dict:
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(
            async_get_session(
                http=http,
                oauth_client=oauth_client,
                headers=headers,
            ),
            loop,
        )
        result = future.result()  # Espera el resultado
        return result
    except RuntimeError:
        return asyncio.run(
            async_get_session(
                http=http,
                oauth_client=oauth_client,
                headers=headers,
            )
        )


async def async_get_session(
    http: str,
    oauth_client: OAuthClient,
    headers: dict[str, str] | None = None,
):
    # CLEANUP IMPLEMENTATION CHANGE:
    # Generate session key for tracking active connections
    session_key = f"{http}_{id(oauth_client)}_{id(headers)}"
    
    # Connect to a streamable HTTP server
    oauth: OAuthClientProvider | None = (
        oauth_client.oauth if oauth_client is not None else None
    )
    
    # CLEANUP IMPLEMENTATION CHANGE:
    # Instead of using context managers that close immediately,
    # manually manage the connection lifecycle for later cleanup
    connection = streamablehttp_client(url=http, auth=oauth, headers=headers)
    read_stream, write_stream, client = await connection.__aenter__()
    
    # Create session
    session = ClientSession(read_stream, write_stream)
    await session.__aenter__()
    
    # CLEANUP IMPLEMENTATION CHANGE:
    # Store active session references for cleanup tracking
    # This allows close_session() to properly terminate connections
    _active_sessions[session_key] = (connection, session, client)
    
    try:
        # Initialize the connection
        await session.initialize()
        # Generate data
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
        raise e


async def close_session(server: dict) -> None:
    """
    Close HTTP stream session for the given server.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function closes HTTP/WebSocket connections for a specific MCP server.
    It reconstructs the session key from server configuration and calls
    close_session_by_key to perform the actual cleanup.
    
    Args:
        server (dict): Server configuration containing connection details
    """
    # Reconstruct session key from server config
    http = server.get("httpstream-url", "")
    oauth_client = server.get("oauth_client")
    headers = server.get("headers")
    
    session_key = f"{http}_{id(oauth_client)}_{id(headers)}"
    
    await close_session_by_key(session_key)


async def close_session_by_key(session_key: str) -> None:
    """
    Close session by its key.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function performs the actual cleanup of HTTP/WebSocket connections.
    It properly closes the session and connection using their __aexit__ methods
    and removes the session from the active sessions dictionary.
    
    Args:
        session_key (str): The session key to close
    """
    if session_key in _active_sessions:
        connection, session, client = _active_sessions[session_key]
        
        try:
            # Close session properly using context manager protocol
            await session.__aexit__(None, None, None)
        except Exception:
            pass  # Ignore cleanup errors
        
        try:
            # Close connection properly using context manager protocol
            await connection.__aexit__(None, None, None)
        except Exception:
            pass  # Ignore cleanup errors
        
        # Remove from active sessions tracking
        del _active_sessions[session_key]


async def close_all_sessions() -> None:
    """
    Close all active HTTP sessions.
    
    NEW FUNCTION ADDED FOR CLEANUP IMPLEMENTATION:
    This function closes all currently active HTTP/WebSocket sessions.
    Useful for complete cleanup when shutting down the application.
    """
    session_keys = list(_active_sessions.keys())
    for session_key in session_keys:
        await close_session_by_key(session_key)
