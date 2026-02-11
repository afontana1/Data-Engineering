from mcp_oauth import OAuthClient
from abc import ABC, abstractmethod


class Service(ABC):
    """Base class for all services (Tool, Resource, Prompt)."""

    def __init__(self, data, server: dict):
        self.protocol: str | None = server.get("protocol", None)

        self.http: str | None = (
            server["httpstream-url"] if self.protocol == "httpstream" else None
        )
        self.data = data
        self.name: str = data.name
        self.description: str = data.description
        self.args: dict[str, any] = None
        self.server: dict = server
        self.oauth_client: OAuthClient | None = server["oauth_client"]
        self.headers: dict[str, str] = server.get("headers", None)

    def __str__(self):
        return str(
            {
                "name": self.name,
                "description": self.description,
                "args": self.args,
            }
        )

    @abstractmethod
    def __call__(self, args: dict[str, any]):
        pass
