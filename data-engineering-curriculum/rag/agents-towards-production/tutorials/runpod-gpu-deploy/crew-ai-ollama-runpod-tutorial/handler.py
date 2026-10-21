"""RunPod handler for CrewAI blog generation."""

import runpod
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import os

# Global setup to load models and configurations only once to improve performance
# Configure Ollama LLM
llm = LLM(model="ollama/openhermes", base_url="http://localhost:11434")

# Create a pseudo-research tool that returns fake information
@tool("Research Tool")
def fake_research(topic: str) -> str:
    """
    Pretends to search for information about a topic. 
    Will always return some fake pre-defined content.
    """
    print(f"\n[LOG] Researching topic: {topic}")
    
    # Dictionary of fake research results for different topics
    fake_results = {
        "artificial intelligence": """
        Fact 1: AI adoption increased by 45% in 2024
        Fact 2: 78% of Fortune 500 companies now use AI in their operations
        Fact 3: The global AI market is projected to reach $1.3 trillion by 2030
        Fact 4: Neural networks can now recognize patterns with 99.8% accuracy
        """,
        "climate change": """
        Fact 1: Global temperatures have risen 1.2°C since pre-industrial times
        Fact 2: 67% of consumers prefer eco-friendly products
        Fact 3: Renewable energy costs fell by 82% between 2010-2024
        Fact 4: Carbon capture technology efficiency improved 40% last year
        """,
        "cryptocurrency": """
        Fact 1: 24% of millennials now own some form of cryptocurrency
        Fact 2: The average crypto transaction takes 12 minutes to process
        Fact 3: Blockchain energy usage decreased 35% with new protocols
        Fact 4: Decentralized finance grew 300% in transaction volume since 2023
        """,
        "health": """
        Fact 1: Telemedicine usage increased 280% since 2020
        Fact 2: 55% of adults track their health using wearable devices
        Fact 3: Precision medicine reduced adverse drug reactions by 42%
        Fact 4: Preventive healthcare saves an average of $3,700 per patient yearly
        """
    }
    
    # Default response if topic isn't in our dictionary
    default_response = """
    Fact 1: 82% of industry leaders consider this topic important
    Fact 2: Research spending in this area grew 34% last year
    Fact 3: Consumer interest in this topic has increased 56% since 2022
    Fact 4: Experts predict significant advancements in the next 5 years
    """
    
    # Check for the topic in our fake results (case insensitive)
    for key in fake_results:
        if key in topic.lower():
            return fake_results[key]
            
    # If no specific match, return the default response
    return default_response

# Create blog writer agent - done once at service startup
blog_writer = Agent(
    role="Blog Writer",
    goal="Write engaging and informative blog posts on various topics",
    backstory="""
    You are a professional blog writer with years of experience creating 
    content that captivates readers. You have a knack for turning complex
    topics into accessible and interesting articles. Your blog posts are
    known for being well-researched, engaging, and having a clear structure.
    """,
    tools=[fake_research],
    verbose=True,
    llm=llm
)

def create_blog_post(topic):
    """Creates a blog post on the given topic using CrewAI"""
    # Create the task for our topic
    blog_task = Task(
        description=f"""
        Write a blog post about {topic}.
        
        Your blog should:
        1. Have an attention-grabbing title
        2. Include a brief introduction that hooks the reader
        3. Present 3-4 main points supported by research
        4. End with a conclusion and potentially a call to action
        
        Use the Research Tool to gather facts about {topic}.
        """,
        expected_output="A well-structured blog post of approximately 500 words",
        agent=blog_writer
    )
    
    # Create the crew with just our blog writer
    crew = Crew(
        agents=[blog_writer],
        tasks=[blog_task],
        verbose=True,
        llm=llm
    )
    
    # Generate the blog post
    print(f"Creating blog about: {topic}")
    result = crew.kickoff()
    return result.raw

def handler(job):
    """Handler function that will be used to process jobs."""
    job_input = job["input"]
    
    # Extract the topic from job input, default to "technology" if not provided
    topic = job_input.get("topic", "technology")
    
    try:
        # Generate blog post using CrewAI
        blog_post = create_blog_post(topic)
        
        # Return successful response
        return {
            "status": "success",
            "blog_post": blog_post
        }
    except Exception as e:
        # Return error response if something goes wrong
        return {
            "status": "error",
            "message": str(e)
        }


runpod.serverless.start({"handler": handler})
