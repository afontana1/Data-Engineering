from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool

import yaml_reader

YAML_FILE_PATH = "prompts.yaml"


class AgentHelper:
    """
    This class helps create and manage different agents (tools and models)
    used for processing information retrieval tasks.

    Args:
        model (str): Name of the large language model to be used.
        url (str, optional): Base url of the Ollama server. Defaults to "http://localhost:11434".
    """

    def __init__(self, model, url="http://localhost:11434"):
        self.yaml_config_reader = yaml_reader.YamlConfigReader(YAML_FILE_PATH)
        self.model = model
        self.ollama_url = url

    def get_llm(
        self,
        model,
        format="json",
        temperature=0,
    ):
        """
        Gets a ChatOllama instance for the specified model.

        Args:
            model (str): Name of the large language model.
            format (str, optional): Output format for the Ollama. Defaults to "json".
            temperature (float, optional): Temperature to control randomness
            of the generation. Defaults to 0.

        Returns:
            ChatOllama: A ChatOllama instance.
        """
        return ChatOllama(
            base_url=self.ollama_url,
            model=model,
            format=format,
            temperature=temperature,
            timeout=5000,
        )

    def create_agent(self, prompt_template, output_parser):
        """
        Creates an agent by chaining a prompt template, large language model, and output parser.

        Args:
            prompt_template (PromptTemplate): The prompt template to be used.
            output_parser (OutputParser): The output parser to be used.

        Returns:
            Agent: A Langchain agent.
        """
        llm = self.get_llm(
            self.model,
            format="json" if isinstance(output_parser, JsonOutputParser) else None,
        )
        return prompt_template | llm | output_parser

    def format_docs(self, docs):
        """
        Formats a list of documents into a single string with each document separated by newlines.

        Args:
            docs (list): A list of documents.

        Returns:
            str: A string with formatted documents.
        """
        return "\n\n".join(doc.page_content for doc in docs)

    def get_agents(self):
        """
        Creates and returns a collection of agents (tools and models)
          for various information retrieval tasks.

        Returns:
            tuple: A tuple containing various agents (tools and models).
        """
        # Retrieval Grader
        retrieval_grader = self.create_agent(
            PromptTemplate(
                template=self.yaml_config_reader.get_prompt_template(
                    "retrieval_grader"
                ),
                input_variables=["question", "document"],
            ),
            JsonOutputParser(),
        )

        ### Generate
        # Chain
        rag_chain = self.create_agent(
            PromptTemplate(
                template=self.yaml_config_reader.get_prompt_template("rag_chain"),
                input_variables=["question", "document"],
            ),
            StrOutputParser(),
        )

        summary_chain = load_summarize_chain(
            self.get_llm(self.model, self.ollama_url),
            chain_type="map_reduce",
            verbose=False,
        )

        ### Hallucination Grader
        hallucination_grader = self.create_agent(
            PromptTemplate(
                template=self.yaml_config_reader.get_prompt_template(
                    "hallucination_grader"
                ),
                input_variables=["generation", "documents"],
            ),
            JsonOutputParser(),
        )

        ### Answer Grader
        answer_grader = self.create_agent(
            PromptTemplate(
                template=self.yaml_config_reader.get_prompt_template("answer_grader"),
                input_variables=["generation", "documents"],
            ),
            JsonOutputParser(),
        )

        ### Search
        search = GoogleSearchAPIWrapper()

        web_search_tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=search.run,
        )

        return (
            retrieval_grader,
            summary_chain,
            rag_chain,
            hallucination_grader,
            answer_grader,
            web_search_tool,
        )
