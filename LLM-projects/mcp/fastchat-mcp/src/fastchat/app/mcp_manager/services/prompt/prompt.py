from mcp_oauth import OAuthClient
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import shutil
import os


from ..service import Service
from .....utils.stdio_session_params import get_stdio_session_params


class Prompt(Service):
    """Represents a prompt that can be called with arguments."""

    def __init__(self, data, server):
        super().__init__(data, server)
        self.args: list[dict] = [
            {"name": arg.name, "type": "string"} for arg in data.arguments
        ]

    async def __call__(self, args: dict[str, any]):
        return await self.get(args)

    async def get(self, args: dict[str, any]):
        args = {key: str(args[key]) for key in args.keys()}

        if self.protocol == "httpstream":
            return await self.__httpstream_get(
                self.http,
                self.name,
                args,
                self.oauth_client,
                self.headers,
            )

        if self.protocol == "stdio":
            return await self.__stdio_get(
                promptname=self.name,
                args=args,
                server=self.server,
            )

    async def __httpstream_get(
        self,
        http: str,
        promptname: str,
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

                # get a prompt
                prompt_result = await session.get_prompt(
                    name=promptname,
                    arguments=args,
                )
                return prompt_result.messages

    async def __stdio_get(
        self,
        promptname: str,
        args: dict,
        server: dict,
    ):
        server_params: StdioServerParameters = get_stdio_session_params(server)
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # get a prompt
                prompt_result = await session.get_prompt(
                    name=promptname,
                    arguments=args,
                )
                return prompt_result.messages
