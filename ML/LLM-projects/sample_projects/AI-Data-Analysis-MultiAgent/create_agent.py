from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai import ChatOpenAI
from typing import List
from langchain.tools import tool
import os
from logger import setup_logger

# Set up logger
logger = setup_logger()

@tool
def list_directory_contents(directory: str = './data_storage/') -> str:
    """
    List the contents of the specified directory.
    
    Args:
        directory (str): The path to the directory to list. Defaults to the data storage directory.
    
    Returns:
        str: A string representation of the directory contents.
    """
    try:
        logger.info(f"Listing contents of directory: {directory}")
        contents = os.listdir(directory)
        logger.debug(f"Directory contents: {contents}")
        return f"Directory contents :\n" + "\n".join(contents)
    except Exception as e:
        logger.error(f"Error listing directory contents: {str(e)}")
        return f"Error listing directory contents: {str(e)}"

def create_agent(
    llm: ChatOpenAI,
    tools: list[tool],
    system_message: str,
    team_members: list[str],
    working_directory: str = './data_storage/'
) -> AgentExecutor:
    """
    Create an agent with the given language model, tools, system message, and team members.
    
    Parameters:
        llm (ChatOpenAI): The language model to use for the agent.
        tools (list[tool]): A list of tools the agent can use.
        system_message (str): A message defining the agent's role and tasks.
        team_members (list[str]): A list of team member roles for collaboration.
        working_directory (str): The directory where the agent's data will be stored.
        
    Returns:
        AgentExecutor: An executor that manages the agent's task execution.
    """
    
    logger.info("Creating agent")

    # Ensure the ListDirectoryContents tool is available
    if list_directory_contents not in tools:
        tools.append(list_directory_contents)

    # Prepare the tool names and team members for the system prompt
    tool_names = ", ".join([tool.name for tool in tools])
    team_members_str = ", ".join(team_members)

    # List the initial contents of the working directory
    initial_directory_contents = list_directory_contents(working_directory)

    # Create the system prompt for the agent
    system_prompt = (
        "You are a specialized AI assistant in a data analysis team. "
        "Your role is to complete specific tasks in the research process. "
        "Use the provided tools to make progress on your task. "
        "If you can't fully complete a task, explain what you've done and what's needed next. "
        "Always aim for accurate and clear outputs. "
        f"You have access to the following tools: {tool_names}. "
        f"Your specific role: {system_message}\n"
        "Work autonomously according to your specialty, using the tools available to you. "
        "Do not ask for clarification. "
        "Your other team members (and other teams) will collaborate with you based on their specialties. "
        f"You are chosen for a reason! You are one of the following team members: {team_members_str}.\n"
        f"The initial contents of your working directory are:\n{initial_directory_contents}\n"
        "Use the ListDirectoryContents tool to check for updates in the directory contents when needed."
    )

    # Define the prompt structure with placeholders for dynamic content
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("ai", "hypothesis: {hypothesis}"),
        ("ai", "process: {process}"),
        ("ai", "process_decision: {process_decision}"),
        ("ai", "visualization_state: {visualization_state}"),
        ("ai", "searcher_state: {searcher_state}"),
        ("ai", "code_state: {code_state}"),
        ("ai", "report_section: {report_section}"),
        ("ai", "quality_review: {quality_review}"),
        ("ai", "needs_revision: {needs_revision}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent using the defined prompt and tools
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    
    logger.info("Agent created successfully")
    
    # Return an executor to manage the agent's task execution
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False)


def create_supervisor(llm: ChatOpenAI, system_prompt: str, members: list[str]) -> AgentExecutor:
    # Log the start of supervisor creation
    logger.info("Creating supervisor")
    
    # Define options for routing, including FINISH and team members
    options = ["FINISH"] + members
    
    # Define the function for routing and task assignment
    function_def = {
        "name": "route",
        "description": "Select the next role and assign a task.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
                "task": {
                    "title": "Task",
                    "type": "string",
                    "description": "The task to be performed by the selected agent"
                }
            },
            "required": ["next", "task"],
        },
    }
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next? "
                "Or should we FINISH? Select one of: {options}. "
                "Additionally, specify the task that the selected role should perform."
            ),
        ]
    ).partial(options=str(options), team_members=", ".join(members))
    
    # Log successful creation of supervisor
    logger.info("Supervisor created successfully")
    
    # Return the chained operations
    return (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )

from core.state import NoteState
from langchain.output_parsers import PydanticOutputParser

def create_note_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
) -> AgentExecutor:
    """
    Create a Note Agent that updates the entire state.
    """
    logger.info("Creating note agent")
    parser = PydanticOutputParser(pydantic_object=NoteState)
    output_format = parser.get_format_instructions()
    escaped_output_format = output_format.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt+"\n\nPlease format your response as a JSON object with the following structure:\n"+escaped_output_format),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    logger.debug(f"Note agent prompt: {prompt}")
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    logger.info("Note agent created successfully")
    return AgentExecutor.from_agent_and_tools(
        agent=agent, 
        tools=tools, 
        verbose=False,
    )

logger.info("Agent creation module initialized")