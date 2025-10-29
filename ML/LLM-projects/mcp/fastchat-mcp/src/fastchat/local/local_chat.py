import asyncio

from ..app.chat.chat import Fastchat
from ..utils.clear_console import clear_console
from ..config.llm_config import ConfigGPT, ConfigLLM
from ..config.logger import logger
import os


class TerminalChat:
    def __init__(
        self,
        model: str = ConfigGPT.DEFAULT_MODEL_NAME,
        extra_reponse_system_prompts: list[str] = [],
        extra_selection_system_prompts: list[str] = [],
        aditional_servers: dict = {},
        len_context: int = ConfigLLM.DEFAULT_HISTORY_LEN,
        logger_lv: str = "ERROR",
    ):
        """
        Initialize the class with model configuration and system prompts.
        Args:
            model (str): The name of the model to use. Defaults to ConfigGPT.DEFAULT_MODEL_NAME.
            extra_reponse_system_prompts (list[str]): Additional system prompts for responses. Defaults to an empty list.
            extra_selection_system_prompts (list[str]): Additional system prompts for MCP services selection. Defaults to an empty list.
            len_context (int): The maximum length of the context history. Defaults to ConfigLLM.DEFAULT_HISTORY_LEN.
        """

        self.model: str = model
        self.extra_reponse_system_prompts: list[str] = extra_reponse_system_prompts
        self.extra_selection_system_prompts: list[str] = extra_selection_system_prompts
        self.aditional_servers: dict = aditional_servers
        self.len_context: int = len_context
        logger.setLevel(logger_lv)

    def open(self):
        return asyncio.run(self.__open())

    async def __open(self):
        """
        ### open_local_chat
        - Launches an interactive local chat session in the console.
        - The conversation is also recorded in Markdown format. When the user exits (by typing 'exit' or pressing Enter),
        the chat history is saved to a Markdown file in the 'chats' directory, using the first query as the filename.
        """

        clear_console()
        chat: Fastchat = Fastchat(
            model=self.model,
            extra_reponse_system_prompts=self.extra_reponse_system_prompts,
            extra_selection_system_prompts=self.extra_reponse_system_prompts,
            aditional_servers=self.aditional_servers,
            len_context=self.len_context,
        )
        await chat.initialize()
        print("\n")

        md: str = ""
        filename: str | None = None
        sep = os.path.sep

        while True:
            query = input("> ")
            if query == "exit" or query == "":
                if md != "":
                    chats_path = f"{os.getcwd()}{sep}chats{sep}"
                    os.makedirs(os.path.dirname(chats_path), exist_ok=True)
                    with open(f"{chats_path}{filename}.md", "w") as file:
                        file.write(md)
                break

            if filename is None:
                filename = f"{query[:15]}..."

            md += f"# {query}"
            index = 1
            async for step in chat(query):
                md += str(step)

                if step.type == "response":
                    if step.json["first_chunk"]:
                        print(f"<< {step.response}", end="")
                    else:
                        print(f"{step.response}", end="")

                if step.type == "query":
                    print(f">> {step.query}")
                    index = 1
                if step.type == "data":
                    print(f'   {str(step).replace("**", "").replace("- ", "• ")}')
                if step.type == "step":
                    print(f"  {index}. {step.step}")
                    index += 1
            md += "\n"
