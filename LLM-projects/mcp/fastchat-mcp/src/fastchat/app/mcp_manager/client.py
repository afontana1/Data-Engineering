import asyncio
from .servers import Servers
from .sessions import httpstrem, stdio
from .services import Tool, Resource, Prompt
from ...config.logger import logger, CustomFormatter, LoggerFeatures


class ClientManagerMCP:
    """
    ClientManagerMCP is responsible for managing and interacting with tools, resources, and prompts
    provided by multiple MCP (Multi-Component Platform) servers. It handles the initialization,
    refreshing, and retrieval of these components, as well as facilitating their invocation.
    
    CLEANUP IMPLEMENTATION CHANGES:
    - Added close() method to properly shutdown all MCP server connections
    - Added context manager support (__aenter__, __aexit__) for automatic cleanup
    - Implemented __close_all_sessions() to handle both HTTP and stdio session cleanup
    - Clear all cached data (tools, resources, prompts) on close to prevent memory leaks
    
    Attributes:
        app_name (str): The name of the application using the manager.
        tools (dict[str, Tool]): Dictionary of available tools, keyed by server and tool name.
        resources (dict[str, Resource]): Dictionary of available resources, keyed by server and resource name.
        prompts (dict[str, Prompt]): Dictionary of available prompts, keyed by server and prompt name.
    ## Methods
        close(): NEW - Properly close all MCP server connections and cleanup resources
        call_tool(name: str, args: dict) -> str | None:
            Calls a tool by name with the provided arguments.
        read_resource(name: str, args: dict) -> str | None:
            Reads a resource by name with the provided arguments.
        get_prompt(name: str, args: dict) -> dict:
            Retrieves a prompt by name with the provided arguments.
        refresh_data():
            Initializes or refreshes the lists of tools, resources, and prompts from all registered MCP servers.
        service_type(service_key: str) -> str:
            Determines whether a given service key corresponds to a tool or a resource.
        get_services() -> list[dict[str, any]]:
            Returns a list of dictionaries representing the available services.
        get_prompts() -> list[dict[str, any]]:
            Returns a list of dictionaries representing the available prompts.
    ## Private Methods
        __get_session(server: dict) -> dict:
            Establishes a session with a given server and retrieves its available tools, resources, and prompts.
    ## Usage
        Instantiate ClientManagerMCP to manage and interact with MCP server components in a unified way.
    """

    INSTANCE = None

    def __init__(
        self,
        aditional_servers: dict = {},
        print_logo: bool = True,
    ):
        self.tools: dict[str, Tool] | None = {}
        self.resources: dict[str, Resource] | None = {}
        self.prompts: dict[str, Prompt] | None = {}

        self.__services: list[dict] = []
        """List of services as strings to be passed to the LLM"""
        self.__prompts_context: list[dict] = []
        """List of prompts as strings to be passed to the LLM"""
        self.__print_logo: bool = print_logo

        self.aditional_servers: dict = aditional_servers

    async def initialize(self) -> None:
        await self.refresh_data()

    async def refresh_data(self) -> None:
        """Initialize or refresh the lists of tools, resources, and prompts from all registered MCP servers."""
        # This method should be implemented to populate tools, resources, and prompts
        pass
        ClientManagerMCP.INSTANCE = self

    # region SINGLETON
    # async def initialize(self) -> None:
    #     if ClientManagerMCP.INSTANCE is None:
    #         await self.refresh_data()
    #         ClientManagerMCP.INSTANCE = self
    #     else:
    #         self.tools = ClientManagerMCP.INSTANCE.tools
    #         self.resources = ClientManagerMCP.INSTANCE.resources
    #         self.prompts = ClientManagerMCP.INSTANCE.prompts
    # endregion

    
    async def close(self) -> None:
        """
        Properly close all MCP server connections and cleanup resources.
        
        NEW METHOD ADDED FOR CLEANUP IMPLEMENTATION:
        This method ensures all active MCP sessions are properly terminated
        and all cached data is cleared to prevent memory leaks.
        
        What it does:
        1. Closes all HTTP stream sessions (WebSocket/HTTP connections)
        2. Closes all stdio sessions (subprocess connections)  
        3. Clears all cached tools, resources, and prompts
        4. Clears internal service and prompt context lists
        5. Resets singleton instance to None
        """
        # Close all active sessions with MCP servers
        await self.__close_all_sessions()
        
        # Clear all cached data to prevent memory leaks
        self.tools.clear() if self.tools else None
        self.resources.clear() if self.resources else None
        self.prompts.clear() if self.prompts else None
        
        # Clear internal service caches
        self.__services.clear()
        self.__prompts_context.clear()
        
        # Clear singleton instance reference
        ClientManagerMCP.INSTANCE = None
        
        logger.info("ClientManagerMCP closed successfully")

    async def __close_all_sessions(self) -> None:
        """
        Close all active sessions with MCP servers.
        
        NEW METHOD ADDED FOR CLEANUP IMPLEMENTATION:
        This method iterates through all configured MCP servers and calls
        the appropriate close_session function based on the protocol type.
        
        Handles two types of MCP connections:
        1. httpstream - HTTP/WebSocket connections 
        2. stdio - Subprocess connections
        """
        mcp_servers: dict[str, dict] = Servers(aditional_servers=self.aditional_servers).mcp_servers or {}
        
        for server_key in mcp_servers.keys():
            server = {"key": server_key} | mcp_servers[server_key]
            
            try:
                if server["protocol"] == "httpstream":
                    # Close HTTP/WebSocket session
                    await httpstrem.close_session(server)
                elif server["protocol"] == "stdio":
                    # Close subprocess session
                    await stdio.close_session(server)
                    
                logger.info(
                    f"Closed connection with server {CustomFormatter.green}{server_key}{CustomFormatter.reset}"
                )
            except Exception as e:
                logger.error(
                    f"Error closing connection with server {CustomFormatter.bold_red}{server_key}{CustomFormatter.reset}: {e}"
                )

    async def __aenter__(self):
        """
        Context manager entry point.
        
        NEW METHOD ADDED FOR CLEANUP IMPLEMENTATION:
        Enables async context manager support for automatic resource management.
        When entering an 'async with' block, this method initializes the 
        ClientManagerMCP instance.
        
        Returns:
            self: The initialized ClientManagerMCP instance
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        
        NEW METHOD ADDED FOR CLEANUP IMPLEMENTATION:
        Enables async context manager support for automatic resource management.
        When exiting an 'async with' block, this method automatically calls
        close() to ensure proper cleanup, even if an exception occurs.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        await self.close()

    async def call_tool(self, name: str, args: dict) -> str | None:
        return await self.tools[name](args)

    async def read_resource(self, name: str, args: dict) -> str | None:
        return await self.resources[name](args)

    async def get_prompt(self, name: str, args: dict) -> dict:
        return await self.prompts[name](args)

    async def refresh_data(self):
        """
        ### Refresh Datas
        - Initializes or refreshes the lists of tools, resources, and prompts provided by each mcp server,
        organizing them into dictionaries.
        - For each registered MCP servers, retrieves their available tools, resources,
        and prompts via a session, and stores them in the corresponding self dictionaries.
        - If a session cannot be established with a server, that server is skipped.
        """
        if self.__print_logo:
            print(LoggerFeatures.LOGO)

        self.tools, self.resources, self.prompts = ({}, {}, {})
        mcp_servers: dict[str, dict] = Servers(aditional_servers=self.aditional_servers).mcp_servers

        for server_key in mcp_servers.keys():
            server = {"key": server_key} | mcp_servers[server_key]
            session = await self.__get_session(server)
            if session is None:
                continue

            for tool in session["tools"]:
                self.tools[f"{server_key}_{tool.name}"] = Tool(data=tool, server=server)
            for resource in session["resources"]:
                self.resources[f"{server_key}_{resource.name}"] = Resource(
                    data=resource, server=server
                )

            for prompt in session["prompts"]:
                self.prompts[f"{server_key}_{prompt.name}"] = Prompt(
                    data=prompt, server=server
                )

    async def __get_session(self, server: dict) -> dict:
        try:
            session: dict = {}

            if server["protocol"] == "httpstream":
                session = await httpstrem.async_get_session(
                    server["httpstream-url"],
                    server["oauth_client"],
                    headers=server.get("headers", None),
                )
            elif server["protocol"] == "stdio":
                session = await stdio.async_get_session(server=server)
            else:
                logger.error(
                    f"Unsupported protocol type {CustomFormatter.bold_red}{server['protocol']}{CustomFormatter.reset} for server {server['key']}"
                )
                return None

            logger.info(
                f"Establish connection with server {CustomFormatter.green}{server['key']}{CustomFormatter.reset} successfully."
            )
            return session
        except Exception as e:
            logger.error(
                f"Failed to establish connection with server {CustomFormatter.bold_red}{server['key']}{CustomFormatter.reset}. Cause: {e}"
            )
            return None

    def service_type(self, service_key: str) -> str:
        """
        Determine the type of service associated with the given service key.
        Args:
            service_key (str): The key identifying the service.
        Returns:
            str: "tool" if the service key corresponds to a tool, "resource" if it corresponds to a resource.
        """

        if service_key in self.tools.keys():
            return "tool"
        if service_key in self.resources.keys():
            return "resource"

    def get_services(self) -> list[dict[str, any]]:
        """
        Returns a list of dictionaries representing the available services. Creates
        a dictionary for each service with the service name as the key and its string
        representation as the value.
        Returns:
            list[dict]: A list of dictionaries, each containing a service name
            and its corresponding string representation.
        """

        if len(self.__services) != len(self.tools) + len(self.resources):
            services = self.tools | self.resources
            self.__services = [
                {service: str(services[service])} for service in services.keys()
            ]

        return self.__services

    def get_prompts(self) -> list[dict[str, any]]:
        """
        Returns a list of prompt dictionaries, ensuring each prompt is represented as a dictionary
        with string values.
        Returns:
            list[dict]: A list of dictionaries containing the current prompts.
        """

        if len(self.__prompts_context) != len(self.prompts):
            self.__prompts_context = [
                {key: str(self.prompts[key])} for key in self.prompts.keys()
            ]
        return self.__prompts_context
