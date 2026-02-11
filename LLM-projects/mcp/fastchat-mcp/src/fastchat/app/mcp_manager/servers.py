import os
import json
from mcp_oauth import OAuthClient
from ...config.logger import logger


class Servers:
    """
    Manages server configurations and OAuth clients for the fastchat-mcp application.
    This class loads server credentials and configuration from a JSON file, initializes
    OAuth clients for each server, and provides access to server information.
    Attributes:
        json_config (dict): The loaded configuration from the JSON file.
        app_name (str): The name of the application.
        mcp_servers (dict[str, dict] | None): Dictionary containing server configurations.
    Methods:
        __init__(config_file_path: str = "fastchat.config.json", app_name: str = "fastchat-mcp"):
            Initializes the Servers instance, loads configuration, and sets up servers.
        __load_config_file(config_file_path: str):
            Loads and parses the configuration JSON file.
        __load_servers():
            Loads server credentials from the configuration and initializes OAuth clients.
        __create_oauth_client(server: dict[str, dict]) -> None:
            Creates an OAuth client for the specified server using provided credentials.
    """

    def __init__(
        self,
        config_file_path: str = "fastchat.config.json",
        app_name: str = "fastchat-mcp",
        aditional_servers: dict = {},
    ):
        """
        Initializes the Servers instance.
        Loads the configuration from the specified JSON file, sets the application name,
        and initializes the server credentials and OAuth clients.
        Args:
            config_file_path (str): Path to the configuration JSON file.
            app_name (str): Name of the application.
        """
        # self.config_file_path: str = config_file_path
        self.json_config: dict = self.__load_config_file(
            config_file_path=config_file_path
        )
        self.app_name = (
            self.json_config["app_name"] if "app_name" in self.json_config else app_name
        )
        self.mcp_servers: dict[str, dict] | None = {}
        self.__load_servers(aditional_servers)

    def __load_config_file(self, config_file_path: str):
        """
        Loads and parses the configuration JSON file.
        Args:
            config_file_path (str): Path to the configuration JSON file.
        Returns:
            dict: Parsed configuration data.
        """

        path = f"{os.getcwd()}{os.path.sep}{config_file_path}"
        if not os.path.exists(path=path):
            logger.warning("config file does not exist")
            return {}

        with open(path, "r") as file:
            json_config: dict = json.loads(file.read())
        return json_config

    def __load_servers(self, aditional_servers: dict = {}):
        """
        Loads server credentials from the configuration.
        Initializes OAuth clients for each server defined in the configuration file.
        """

        self.mcp_servers = self.json_config["mcp_servers"] | aditional_servers

        for server in self.mcp_servers.values():
            self.__create_oauth_client(server=server)

    def __create_oauth_client(self, server: dict[str, dict]) -> None:
        """
        Creates an OAuth client for the specified server.
        Uses the credentials provided in the configuration to generate an OAuth client
        and attaches it to the server's configuration.
        Args:
            server (dict[str, dict]): Server configuration dictionary.
        """
        oauth_client: OAuthClient | None = None

        server_url: str | None = (
            server["httpstream-url"] if "httpstream-url" in server else None
        )

        if "auth" in server.keys() and (
            "required" in server["auth"].keys() and server["auth"]["required"]
        ):
            auth: dict = server["auth"]
            post_body = auth["post_body"]
            oauth_client = OAuthClient(
                client_name=self.app_name,
                mcp_server_url=server_url,
                body=post_body,
            )

        server["oauth_client"] = oauth_client
