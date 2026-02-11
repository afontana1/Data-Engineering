import json
import uuid
from typing import AsyncGenerator
from mcp.types import PromptMessage
from .message import MessagesSet
from ..client_db.client_db import ClientDB
from .features.llm_provider import LLMProvider
from .features.step import Step, StepMessage, DataStep, ResponseStep, QueryStep
from ..services.llm import LLM
from ..mcp_manager.client import ClientManagerMCP
from ..services.llm.models.openai_service.gpt import GPT
from ...config.llm_config import ConfigGPT, ConfigLLM


class Fastchat:
    """
    Chat class for managing conversational interactions with an LLM (Large Language Model).
    This class orchestrates the process of handling user queries, selecting prompts and services,
    and generating responses using a language model. It supports context management, prompt selection,
    service invocation, and streaming responses in a step-wise manner.
    Args:
        llm_provider (LLMProvider): The provider of language model to use. Default is `LLMProvider.OPENAI`.
        model (str): The model name to use for the LLM. Defaults to ConfigGPT.DEFAULT_MODEL_NAME.
        len_context (int): Maximum length of the conversation history to maintain. Defaults to 10.
        history (list): Initial chat history. Defaults to an empty list.
        id (str | None): Optional identifier for the chat session.
        user_id (str): Optional identifier for the chat session.
    
    ## Methods
        __call__(query: str) -> Generator[Step]:
            Processes a user query through multiple steps, including query analysis,
            prompt selection, service selection, and response generation. Yields Step objects
            representing each stage of the process.
        proccess_query(query: str) -> Generator[Step]:
            Handles the detailed processing of a single query, including updating chat history,
            selecting prompts and services, and generating the final response. Yields Step objects
            for each sub-step in the process.
    """

    def __init__(
        self,
        id: str | None = None,
        model=ConfigGPT.DEFAULT_MODEL_NAME,
        llm_provider: LLMProvider = ConfigLLM.DEFAULT_PROVIDER,
        extra_reponse_system_prompts: list[str] = [],
        extra_selection_system_prompts: list[str] = [],
        aditional_servers: dict = {},
        len_context: int = ConfigLLM.DEFAULT_HISTORY_LEN,
        history: list = [],
        user_id: str = "public",
    ):
        """
        Initialize a Chat instance.
        Args:
            id (str | None, optional): Optional chat session identifier.
            model (str, optional): The model name to use. Defaults to ConfigGPT.DEFAULT_MODEL_NAME.
            llm_provider (LLMProvider, optional): The language model provider. Defaults to LLMProvider.OPENAI.
            extra_reponse_system_prompts (list[str]): Additional system prompts for responses. Defaults to an empty list.
            extra_selection_system_prompts (list[str]): Additional system prompts for MCP services selection. Defaults to an empty list.
            aditional_servers (dic, optional): dictionary of servers with the format: `{server_1:{...server config...}, "server_2":{...}}`
            len_context (int, optional): Maximum number of messages to keep in context. Defaults to 10.
            history (list, optional): Initial chat history. Defaults to empty list.
        """

        self.clientdb: ClientDB = ClientDB()
        self.user_id: str = user_id

        self.id = id if id is not None else str(uuid.uuid4())
        loaded_history = (
            self.clientdb.load_history(chat_id=self.id) if id is not None else []
        )

        self.llm: LLM = GPT(
            max_history_len=len_context,
            model=model,
            chat_history=history + loaded_history,
        )
        self.client_manager_mcp: ClientManagerMCP | None = None  # MCP client manager for handling server connections
        self.extra_reponse_system_prompts: list[dict[str, str]] = [
            {
                "role": "system",
                "content": message,
            }
            for message in extra_reponse_system_prompts
        ]
        self.extra_selection_system_prompts: list[dict[str, str]] = [
            {
                "role": "system",
                "content": message,
            }
            for message in extra_selection_system_prompts
        ]
        self.aditional_servers: dict = aditional_servers

        self.current_messages_set: MessagesSet | None = None

    async def close(self) -> None:
        """
        Properly cleanup and close the Fastchat instance.
        
        This method ensures all active connections and resources are properly closed
        to prevent memory leaks and hanging connections. It should be called when 
        the chat session is no longer needed.
        
        Changes made for cleanup implementation:
        - Added proper MCP client manager cleanup
        - Clear all reference collections to help garbage collection
        - Set client manager to None to prevent further usage
        """
        # Close MCP client manager and all its connections
        # This will close all HTTP/WebSocket connections and stdio processes
        if self.client_manager_mcp is not None:
            await self.client_manager_mcp.close()  # Closes all MCP server connections
            self.client_manager_mcp = None  # Prevent further usage

        # Close LLM client (if tiene método close)
        if hasattr(self.llm, 'close') and callable(getattr(self.llm, 'close')):
            await self.llm.close()
        
        # Clear references to help garbage collection
        # These collections might hold references to large objects
        self.current_messages_set = None
        self.extra_reponse_system_prompts.clear()
        self.extra_selection_system_prompts.clear()
        self.aditional_servers.clear()

    async def __aenter__(self):
        """
        Context manager entry point.
        
        This method is part of the async context manager protocol implementation.
        It automatically initializes the Fastchat instance when entering a 
        'async with' block, ensuring proper setup.
        
        Returns:
            self: The initialized Fastchat instance
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        
        This method is part of the async context manager protocol implementation.
        It automatically calls close() when exiting an 'async with' block,
        ensuring proper cleanup even if an exception occurs.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any) 
            exc_tb: Exception traceback (if any)
        """
        await self.close()

    
    async def initialize(self, print_logo: bool = True) -> None:
        await self.__set_client_manager_mcp(print_logo=print_logo)

    async def __set_client_manager_mcp(self, print_logo: bool) -> None:
        if self.client_manager_mcp is None:
            self.client_manager_mcp = ClientManagerMCP(
                aditional_servers=self.aditional_servers,
                print_logo=print_logo,
            )
            await self.client_manager_mcp.initialize()
            self.llm.set_client_manager_mcp(self.client_manager_mcp)

    ####  FLOW   FLOW   FLOW ####
    async def __call__(self, query: str) -> AsyncGenerator[Step]:
        """
        Processes a user query through the chat pipeline.
        This method analyzes the query, preprocesses it, selects relevant prompts and services,
        and generates a response. The process is broken down into steps, each represented by a Step object,
        which are yielded sequentially to allow for streaming or step-wise processing.
        Args:
            query (str): The user's input query.
        Yields:
            Step: An object representing each stage of the query processing pipeline.
        """

        yield Step(step_type=StepMessage.ANALYZE_QUERY)
        self.current_messages_set = MessagesSet(query=query)

        processed_query: dict = self.llm.preprocess_query(query=query)
        querys: list[str] = processed_query["querys"]
        self.llm.current_language = processed_query["language"]

        self.current_messages_set.selected_querys(querys=querys)

        yield DataStep(data={"querys": querys})

        for query in querys:
            async for step in self.proccess_query(query):
                yield step

        # Save To Database Here
        messsages2save: MessagesSet = self.current_messages_set
        await self.clientdb.save_message(
            chat_id=self.id,
            message_id=messsages2save.id,
            user_id=self.user_id,
            message=messsages2save,
        )
        ###########################

        # self.current_messages_set = None

    async def proccess_query(self, query: str) -> AsyncGenerator[Step]:
        """
        Handles the detailed processing of a single query.
        This method updates the chat history, selects prompts and services based on the query,
        invokes the appropriate service or tool, and generates the final response. Each sub-step
        is yielded as a Step object for granular control and streaming.
        Args:
            query (str): The user's input query.
        Yields:
            Step: An object representing each sub-step of the query processing, including prompt selection,
                  service selection, and response generation.
        """
        client_manager_mcp: ClientManagerMCP = self.client_manager_mcp
        self.llm.append_chat_history()
        yield QueryStep(query)

        self.current_messages_set.append_message({"role": "user", "content": query})

        # region ########### GET PROMTPS ###########
        yield Step(step_type=StepMessage.SELECT_PROMPTS)
        prompts = json.loads(
            self.llm.select_prompts(query, self.extra_selection_system_prompts)
        )["prompt_services"]
        self.current_messages_set.selected_prompts(prompts=prompts)

        if len(prompts) == 0:
            yield DataStep(data={"prompts": None})

        for index, prompt in enumerate(prompts):
            yield DataStep(data={f"prompt {index+1}": prompt["prompt_service"]})

        extra_messages = [
            await client_manager_mcp.prompts[prompt["prompt_service"]](prompt["args"])
            for prompt in prompts
        ]
        extra_messages = [
            prompt_message2dict(message)
            for prompt_message in extra_messages
            for message in prompt_message
        ]
        # endregion ###################################################

        # region ########### SELECT SERVICE AND ARGS ############
        yield Step(step_type=StepMessage.SELECT_SERVICE)
        # Cargar los servicios utiles
        service = json.loads(
            self.llm.select_service(
                query,
                extra_messages=extra_messages + self.extra_selection_system_prompts,
            )
        )
        args = service["args"]
        service = service["service"]
        self.current_messages_set.selected_service(
            service={"service": service, "args": args}
        )
        # endregion ###################################################

        # region ########### RESPONSE ############
        if len(service) == 0:
            yield DataStep(data={"service": None})
            first_chunk = True
            stream = self.llm.simple_query(
                query,
                use_services_contex=True,
                extra_messages=extra_messages + self.extra_reponse_system_prompts,
            )
            response = ""
            for chunk in stream:
                yield ResponseStep(response=chunk, data=None, first_chunk=first_chunk)
                response += chunk if chunk is not None else ""
                first_chunk = False

            self.current_messages_set.append_message(
                {"role": "assistant", "content": response}
            )
            yield ResponseStep(response="\n\n", data=None)

        else:
            yield DataStep(data={"service": service})
            yield DataStep(data={"args": args})
            service = (
                client_manager_mcp.resources[service]
                if (client_manager_mcp.service_type(service) == "resource")
                else (
                    client_manager_mcp.tools[service]
                    if (client_manager_mcp.service_type(service) == "tool")
                    else None
                )
            )

            data = await service(args)
            data = data[0].text
            first_chunk = True
            for chunk in self.llm.final_response(
                query,
                data,
                extra_messages=self.extra_reponse_system_prompts,
            ):
                yield ResponseStep(response=chunk, data=None, first_chunk=first_chunk)
                first_chunk = False
            yield ResponseStep(response="\n\n", data=data)

        # endregion ###################################################


def prompt_message2dict(prompt_message: PromptMessage):
    data: dict = json.loads(prompt_message.content.text)
    return {"role": prompt_message.role, "content": data["content"]["text"]}


""" FLOW
see https://github.com/rb58853/fastchat-mcp/tree/main/doc/FLOW.md
"""
