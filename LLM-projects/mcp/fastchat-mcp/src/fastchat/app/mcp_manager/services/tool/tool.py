from mcp_oauth import OAuthClient
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from .....utils.stdio_session_params import get_stdio_session_params
import os

import asyncio

from ..service import Service

"""
TODO
- Refactorize code, without repetition
"""


class Tool(Service):
    """Represents a tool that can be called with arguments."""

    def __init__(self, data, server):
        super().__init__(data, server)
        self.args: list[dict] = self.__get_args_schema(data=data)

    def __get_args_schema(self, data):
        properties = data.inputSchema["properties"]
        args = []
        for key in properties.keys():
            arg_type = properties[key].get("type", None)
            if arg_type is None:
                if "anyOf" in properties[key]:
                    arg_type = ""
                    for type_ in properties[key]["anyOf"]:
                        arg_type += type_["type"] + " | "
                    arg_type = arg_type[:-3]  # Remove the last " | "
            args.append({"name": key, "type": arg_type})

        return args

    async def __call__(self, args: dict[str, any]):
        return await self.call(args)

    async def call(self, args: dict[str, any]):
        if self.protocol == "httpstream":
            return await self.__httpstream_call(
                self.http,
                self.name,
                args,
                self.oauth_client,
                self.headers,
            )
        if self.protocol == "stdio":
            return await self.__stdio_call(self.name, args, self.server)

    async def __httpstream_call(
        self,
        http: str,
        toolname: str,
        args: dict,
        oauth_client: OAuthClient | None,
        headers: dict[str, str] = None,
    ):
        oauth: OAuthClientProvider = (
            oauth_client.oauth if oauth_client is not None else None
        )
        async with streamablehttp_client(url=http, auth=oauth, headers=headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # Call a tool
                tool_result = await session.call_tool(toolname, args)
                return tool_result.content

    async def __stdio_call(self, toolname: str, args: dict, server: dict):
        server_params: StdioServerParameters = get_stdio_session_params(server)
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Call a tool
                tool_result = await session.call_tool(toolname, args)
                return tool_result.content
