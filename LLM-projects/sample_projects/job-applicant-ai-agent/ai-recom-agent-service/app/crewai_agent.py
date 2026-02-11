import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from app import settings

# Set API keys
os.environ["SERPER_API_KEY"] = str(settings.SERPER_API_KEY)
os.environ["OPENAI_API_KEY"] = str(settings.OPENAI_API_KEY)

# Initialize the search tool
search_tool = SerperDevTool()

# Define the Information Provider agent
info_provider = Agent(
    role='Consultant and Trainer',
    goal='Guide user to complete their tasks in todo list with all relevant information based on user input about their work.',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert consultant, always ready to assist users"
        "by providing them with the most relevant and up-to-date information"
        "based on their work descriptions."
    ),
    tools=[search_tool],
    allow_delegation=False
)

# Email Crafter Agent
email_crafter = Agent(
    role='Email Body Crafter',
    goal='Craft an informal and engaging email body to user to provide information about their todo list task.',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in crafting emails and always ready to assist users"
        "by providing them with the most relevant and up-to-date information"
        "based on their work descriptions."
    ),
    tools=[search_tool],
    allow_delegation=False
)

# Define the task
info_task = Task(
    description=(
        "Take user input describing their todo list task and use it as a search query to find relevant information."
        "Provide a summary or detailed information related to the user's work."
    ),
    expected_output=' Provide a concise summary with relevant details for user to complete their todo.',
    tools=[search_tool],
    agent=info_provider,
    async_execution=False
)

# Craft Email Task
email_task = Task(
    description=(
        "Take the information provided by the Information Provider and craft an email body to user."
    ),
    expected_output='Craft an email body to user to provide guidelines and facts about their todo list task. And encourage to complete the task. Do not Write User Name, Dear or Subject in Email.',
    agent=email_crafter,
    async_execution=False
)

# Create the crew
crew = Crew(
    agents=[info_provider, email_crafter],
    tasks=[info_task, email_task],
    process=Process.sequential
)

# Function to get user input and kickoff the crew
def get_user_input_and_provide_info(user_input: str):

    # Update the task with the user's input
    info_task.description = (
        f"You are an expert consultant who provide/gives suggestions to user about their todo's. "
        f"You will get the todo task details or title and you will use it to curate and share specialized recommendations and consultancy to complete todo. "
        f"Use Search Tool to get latest info when needed. "
        f"USER_TODO: '{user_input}'. "
        f"Provide a concise summary with relevant details for user to complete their todo."
    )

    result = crew.kickoff(inputs={'user_todo_item': user_input})

    print("Relevant Information Retrieved:")

    return result
