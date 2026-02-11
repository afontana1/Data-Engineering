import os
import json
import aiohttp
import requests
from urllib.parse import urljoin
from ..chat.message import MessagesSet
from ...config.logger import logger

ROOT_PATH = "http://127.0.0.1:6543/fastchatdb/"
SAVE_HISTORY = "history/save"
SAVE_MESSAGE = "message/save"
LOAD_HISTORY = "history/load"


class ClientDB:
    def __init__(
        self,
        config_file: str = "fastchat.config.json",
    ):
        self.base_body: dict = {}
        self.base_query: dict = {}

        self.is_none: bool = True
        self.headers: dict | None = None
        self.__load_config(config_file=config_file)

    def __load_config(self, config_file: str):
        """
        Load the configuration from the specified JSON file.
        If the file does not exist, use default values.
        """
        root_path: str = ROOT_PATH
        save_history: str = SAVE_HISTORY
        load_history: str = LOAD_HISTORY
        save_message: str = SAVE_MESSAGE

        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config: dict = json.load(file)

            db_connection: dict = config.get("db_conection")
            if db_connection is not None:
                self.is_none = False

                self.headers = db_connection.get("headers", {})
                self.base_body = db_connection.get("base_body", {})
                self.base_query = db_connection.get("base_query", {})

                root_path = db_connection.get("root_path") or ROOT_PATH

                endpoints: dict = db_connection.get("endpoints")
                if endpoints is not None:

                    save_history_endpoint: dict = endpoints.get("save_history")
                    if save_history_endpoint is not None:
                        save_history = save_history_endpoint.get("path") or save_history

                    load_history_endpoint: dict = endpoints.get("load_history")
                    if load_history_endpoint is not None:
                        load_history = load_history_endpoint.get("path") or load_history

                    save_message_endpoint: dict = endpoints.get("save_message")
                    if save_message_endpoint is not None:
                        save_message = save_message_endpoint.get("path") or save_message

        self.set_database_endpoints_path(
            root_path=root_path,
            save_history=save_history,
            load_history=load_history,
            save_message=save_message,
        )

    def set_database_endpoints_path(
        self,
        root_path: str = ROOT_PATH,
        save_history: str = SAVE_HISTORY,
        load_history: str = LOAD_HISTORY,
        save_message: str = SAVE_MESSAGE,
    ):
        if not root_path.endswith("/"):
            root_path += "/"

        save_history = (
            save_history[1:] if save_history.startswith("/") else save_history
        )
        load_history = (
            load_history[1:] if load_history.startswith("/") else load_history
        )
        save_message = (
            save_message[1:] if save_message.startswith("/") else save_message
        )

        self.save_history_path: str = urljoin(root_path, save_history)
        self.load_history_path: str = urljoin(root_path, load_history)
        self.save_messsage_path: str = urljoin(root_path, save_message)

    async def _post(self, url: str, json_data: dict) -> dict:
        """
        Asynchronously send a POST request to the given URL with the provided JSON data.
        Returns the response as a dictionary.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=self.headers) as resp:
                return await resp.json()

    async def _get(self, url: str, params: dict) -> dict:
        """
        Asynchronously send a GET request to the given URL with the provided query parameters.
        Returns the response as a dictionary.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                return await resp.json()

    def load_history(self, chat_id: str) -> list:
        """
        Load the chat history from the database via the configured endpoint.
        Returns the history as a list if successful, otherwise an empty list.
        """
        if self.is_none:
            return []

        params = self.base_query.copy()
        params.update({"chat_id": chat_id})
        try:
            response = requests.get(
                self.load_history_path, params, headers=self.headers
            )
            if response.get("status") == "success":
                logger.info(f"History for chat_id {chat_id} loaded successfully")
                return response.get("history", [])
        except Exception as e:
            logger.warning(f"Error loading history for chat_id {chat_id}: {e}")
            return []

        return []

    async def save_history(self, chat_id: str, history: list[dict]) -> bool:
        """
        Asynchronously save the chat history to the database via the configured endpoint.
        Returns True if the operation was successful.
        """
        if self.is_none:
            return False

        data = self.base_body.copy()
        data.update({"chat_id": chat_id, "history": history})
        try:
            response = await self._post(self.save_history_path, data)
            logger.info(f"History for chat_id {chat_id} saved successfully")
            return response.get("status") == "success"
        except Exception as e:
            logger.warning(f"Error saving history for chat_id {chat_id}: {e}")
            return False

    async def save_message(
        self,
        chat_id: str,
        message_id: str,
        message: MessagesSet,
        user_id: str = "public",
    ) -> bool:
        """
        Asynchronously save a single message to the database via the configured endpoint.
        Returns True if the operation was successful.
        """
        if self.is_none:
            return False

        data = self.base_body.copy()
        data.update(
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "user_id": user_id,
                "message": message.info,
            }
        )
        try:
            response = await self._post(self.save_messsage_path, data)
            if response.get("status") == "success":
                logger.info(f"Message {message_id} saved to database successfully")
            else:
                logger.warning(
                    f"Error saving message {message_id}: {response.get('message')}"
                )

            return response.get("status") == "success"
        except Exception as e:
            logger.warning(f"Error saving message {message_id}: {e}")

            return False  # Error
