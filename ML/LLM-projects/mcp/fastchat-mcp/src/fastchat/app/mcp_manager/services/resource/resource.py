from mcp_oauth import OAuthClient
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import shutil
import os
from .....utils.stdio_session_params import get_stdio_session_params


from ..service import Service
from . import utils


class Resource(Service):
    """Represents a resource that can be read with arguments."""

    def __init__(self, data, server):
        super().__init__(data, server)
        self.args = utils.get_args_from_uri(data.uriTemplate)
        self.args = [{"name": arg, "type": "string"} for arg in self.args]

    async def __call__(self, args: dict[str, any]):
        return self.read(args)

    async def read(self, args: dict[str, str]):
        uri = self.data.uriTemplate
        for key in args:
            uri = uri.replace("{" + key + "}", str(args[key]))

        if self.protocol == "httpstream":
            return await self.__httpstream_read(
                self.http,
                uri,
                self.oauth_client,
                self.headers,
            )

        if self.protocol == "stdio":
            return await self.__stdio_read(uri=uri, server=self.server)

    async def __httpstream_read(
        self,
        http: str,
        uri: str,
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

                # Read a resource
                resource_result = await session.read_resource(uri)
                return resource_result.contents

    async def __stdio_read(self, uri: str, server: dict):
        server_params: StdioServerParameters = get_stdio_session_params(server)
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Read a resource
                resource_result = await session.read_resource(uri)
                return resource_result.contents
