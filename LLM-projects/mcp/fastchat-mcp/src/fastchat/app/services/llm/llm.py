from collections.abc import Generator
from abc import ABC, abstractmethod

from ...mcp_manager.client import ClientManagerMCP


class LLM(ABC):
    """
    Abstract base class for Language Model (LLM) services.

    This class defines the interface for integrating different LLM backends into the system.
    It provides a standard set of methods that must be implemented by any subclass, ensuring
    consistent behavior across different LLM implementations. The class manages a client
    manager for MCP (Multi-Client Platform) and tracks the current language context.

    Attributes:
        client_manager_mcp (ClientManagerMCP): Manages connections to MCP clients.
        current_language (str): The current language context for the LLM, default is "English".

    Methods:
        preprocess_query(query: str) -> dict:
            Preprocesses the input query to extract relevant information such as language and
            the main content of the query. Returns a dictionary with the extracted components.

        append_chat_history():
            Appends the current query and its context to the chat history, maintaining a record
            of the conversation for context-aware responses.

        select_prompts(query: str) -> str:
            Selects and returns the most appropriate prompts, from mcp servers, based on the user's query. This
            helps in guiding the LLM to generate more relevant responses.

        select_service(query: str, extra_messages: list[dict[str, str]] = []) -> str:
            Determines the most relevant services to use for the given query by analyzing the
            available services from all connected servers. Constructs a prompt with the user's
            query and the list of services, then uses the LLM to select the best services.
            Returns a JSON-formatted string indicating the selected services.

        simple_query(query: str, use_services_contex: bool = False, extra_messages: list[dict[str, str]] = []) -> Generator[str, None]:
            Executes a simple query against the LLM, optionally including service context and
            extra messages. Returns a generator that yields response chunks as they are produced.

        final_response(query: str, data: str | dict, extra_messages: list[dict[str, str]] = []) -> Generator[str, None]:
            Generates the final response to the user based on the original query and any
            additional data or context. Returns a generator that yields the response in chunks.

        close() -> None:
            Cleanup method for releasing LLM-specific resources such as API clients,
            connection pools, or cached data. Should be called when the LLM instance
            is no longer needed.
    """

    def __init__(self):
        self.client_manager_mcp: ClientManagerMCP | None = None
        self.current_language: str = "English"

    def set_client_manager_mcp(self, client_manager_mcp: ClientManagerMCP | None):
        self.client_manager_mcp: ClientManagerMCP = client_manager_mcp

    @abstractmethod
    def preprocess_query(self, query: str) -> dict:
        """
        Preprocesses the input query string to extract relevant information such as the language and the main query content.
        Args:
            query (str): The input query string provided by the user.
        Returns:
            dict: A dictionary containing the extracted language and the processed query parts.
        Note:
            This function is intended to be used as a preprocessing step before passing the query to downstream language model services.
        """
        pass

    @abstractmethod
    def append_chat_history(self):
        """
        Append the current user query to the chat history.
        This method should be called after receiving a new user query to ensure that the conversation history
        is updated accordingly. The implementation is expected to handle the storage (in the llm class instance) of the query
        in the appropriate chat history structure.
        """
        pass

    @abstractmethod
    def select_prompts(self, query: str, extra_messages: list[dict[str, str]]) -> str:
        """
        Selects and returns appropriate prompts, from mcp servers, based on the provided query.
        Args:
            query (str): The input query string for which prompts need to be selected.
        Returns:
            str: The selected prompt(s) relevant to the input query.
            Using the structure: `{"prompts":[name for name in retrived_prompts]}`
        """
        pass

    @abstractmethod
    def select_service(
        self, query: str, extra_messages: list[dict[str, str]] = []
    ) -> str:
        """
        Selects the most relevant services for the given query context by leveraging the available services exposed by each server.
        This function gathers all available services from the client manager, constructs a prompt combining the user's query and the list of services, and then calls the completion endpoint to determine which services are most useful for the given context.
        Args:
            query (str): The user's query for which relevant services need to be selected.
            extra_messages (list[dict[str, str]], optional): Additional messages to include in the context. Defaults to an empty list.
        Returns:
            str: The result of the completion call, typically a JSON-formatted string indicating the selected services.
        """
        pass

    @abstractmethod
    def simple_query(
        self,
        query: str,
        use_services_contex: bool = False,
        extra_messages: list[dict[str, str]] = [],
    ) -> Generator[str, None]:
        """
        Performs a simple query to the language model and returns a generator yielding response chunks.
        Args:
            query (str): The input query string to be processed by the language model.
            use_services_contex (bool, optional): Whether to use additional service context in the query. Defaults to False.
            extra_messages (list[dict[str, str]], optional): Additional messages to include in the conversation context. Each message should be a dictionary with string keys and values. Defaults to an empty list.
        Yields:
            str: Chunks of the response generated by the language model.
        """
        pass

    @abstractmethod
    def final_response(
        self,
        query: str,
        data: str | dict,
        extra_messages: list[dict[str, str]] = [],
    ) -> Generator[str, None]:
        """
        Generate the final response for a given query and data.
        Args:
            query (str): The input query string from the user.
            data (str | dict): The data to be used for generating the response. Can be a string or a dictionary.
            extra_messages (list[dict[str, str]], optional): Additional messages to include in the response context. Defaults to an empty list.
        Yields:
            str: The generated response string(s), yielded one at a time.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Cleanup method for releasing LLM-specific resources.
        
        CLEANUP IMPLEMENTATION METHOD:
        This method should be implemented by each LLM subclass to properly
        clean up any resources specific to that LLM implementation such as:
        - API client connections
        - Connection pools
        - Cached data structures
        - Thread pools or async tasks
        - Authentication tokens
        
        Should be called when the LLM instance is no longer needed to prevent
        resource leaks and ensure proper cleanup.
        """
        pass
