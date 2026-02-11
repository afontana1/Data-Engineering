from enum import Enum
import logging
from typing import Any
import json

# Import MCP server
from mcp.server.models import InitializationOptions
from mcp.types import (
    TextContent,
    Tool,
    Resource,
    Prompt,
    PromptArgument,
    GetPromptResult,
    PromptMessage,
)
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

logger = logging.getLogger(__name__)
logger.info("Starting deep research server")


### Prompt templates
class DeepResearchPrompts(str, Enum):
    DEEP_RESEARCH = "deep-research"


class PromptArgs(str, Enum):
    RESEARCH_QUESTION = "research_question"


PROMPT_TEMPLATE = """
You are a professional researcher tasked with conducting thorough research on a topic and producing a structured, comprehensive report. Your goal is to provide a detailed analysis that addresses the research question systematically.

The research question is:

<research_question>
{research_question}
</research_question>

Follow these steps carefully:

1. <question_elaboration>
   Elaborate on the research question. Define key terms, clarify the scope, and identify the core issues that need to be addressed. Consider different angles and perspectives that are relevant to the question.
</question_elaboration>

2. <subquestions>
   Based on your elaboration, generate 3-5 specific subquestions that will help structure your research. Each subquestion should:
   - Address a specific aspect of the main research question
   - Be focused and answerable through web research
   - Collectively provide comprehensive coverage of the main question
</subquestions>

3. For each subquestion:
   a. <web_search_results>
      Search for relevant information using web search. For each subquestion, perform searches with carefully formulated queries.
      Extract meaningful content from the search results, focusing on:
      - Authoritative sources
      - Recent information when relevant
      - Diverse perspectives
      - Factual data and evidence
      
      Be sure to properly cite all sources and avoid extensive quotations. Limit quotes to less than 25 words each and use no more than one quote per source.
   </web_search_results>

   b. Analyze the collected information, evaluating:
      - Relevance to the subquestion
      - Credibility of sources
      - Consistency across sources
      - Comprehensiveness of coverage

4. Create a beautifully formatted research report as an artifact. Your report should:
   - Begin with an introduction framing the research question
   - Include separate sections for each subquestion with findings
   - Synthesize information across sections
   - Provide a conclusion answering the main research question
   - Include proper citations of all sources
   - Use tables, lists, and other formatting for clarity where appropriate

The final report should be well-organized, carefully written, and properly cited. It should present a balanced view of the topic, acknowledge limitations and areas of uncertainty, and make clear, evidence-based conclusions.

Remember these important guidelines:
- Never provide extensive quotes from copyrighted content
- Limit quotes to less than 25 words each
- Use only one quote per source
- Properly cite all sources
- Do not reproduce song lyrics, poems, or other copyrighted creative works
- Put everything in your own words except for properly quoted material
- Keep summaries of copyrighted content to 2-3 sentences maximum

Please begin your research process, documenting each step carefully.
"""


### Research Processor
class ResearchProcessor:
    def __init__(self):
        self.research_data = {
            "question": "",
            "elaboration": "",
            "subquestions": [],
            "search_results": {},
            "extracted_content": {},
            "final_report": "",
        }
        self.notes: list[str] = []

    def add_note(self, note: str):
        """Add a note to the research process."""
        self.notes.append(note)
        logger.debug(f"Note added: {note}")

    def update_research_data(self, key: str, value: Any):
        """Update a specific key in the research data dictionary."""
        self.research_data[key] = value
        self.add_note(f"Updated research data: {key}")

    def get_research_notes(self) -> str:
        """Return all research notes as a newline-separated string."""
        return "\n".join(self.notes)

    def get_research_data(self) -> dict:
        """Return the current research data dictionary."""
        return self.research_data


### MCP Server Definition
async def main():
    research_processor = ResearchProcessor()
    server = Server("deep-research-server")

    @server.list_resources()
    async def handle_list_resources() -> list[Resource]:
        logger.debug("Handling list_resources request")
        return [
            Resource(
                uri="research://notes",
                name="Research Process Notes",
                description="Notes generated during the research process",
                mimeType="text/plain",
            ),
            Resource(
                uri="research://data",
                name="Research Data",
                description="Structured data collected during the research process",
                mimeType="application/json",
            ),
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        if str(uri) == "research://notes":
            return research_processor.get_research_notes()
        elif str(uri) == "research://data":
            return json.dumps(research_processor.get_research_data(), indent=2)
        else:
            raise ValueError(f"Unknown resource: {uri}")

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        logger.debug("Handling list_prompts request")
        return [
            Prompt(
                name=DeepResearchPrompts.DEEP_RESEARCH,
                description="A prompt to conduct deep research on a question",
                arguments=[
                    PromptArgument(
                        name=PromptArgs.RESEARCH_QUESTION,
                        description="The research question to investigate",
                        required=True,
                    ),
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> GetPromptResult:
        logger.debug(f"Handling get_prompt request for {name} with args {arguments}")
        if name != DeepResearchPrompts.DEEP_RESEARCH:
            logger.error(f"Unknown prompt: {name}")
            raise ValueError(f"Unknown prompt: {name}")

        if not arguments or PromptArgs.RESEARCH_QUESTION not in arguments:
            logger.error("Missing required argument: research_question")
            raise ValueError("Missing required argument: research_question")

        research_question = arguments[PromptArgs.RESEARCH_QUESTION]
        prompt = PROMPT_TEMPLATE.format(research_question=research_question)

        # Store the research question
        research_processor.update_research_data("question", research_question)
        research_processor.add_note(
            f"Research initiated on question: {research_question}"
        )

        logger.debug(
            f"Generated prompt template for research_question: {research_question}"
        )
        return GetPromptResult(
            description=f"Deep research template for: {research_question}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt.strip()),
                )
            ],
        )

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        logger.debug("Handling list_tools request")
        # We're not exposing any tools since we'll be using Claude's built-in web search
        return []

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.debug("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="deep-research-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
