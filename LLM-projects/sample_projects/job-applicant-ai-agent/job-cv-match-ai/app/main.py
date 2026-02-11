import os
from fastapi import FastAPI, File, UploadFile, Form
from crewai import Agent, Task, Crew
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    MDXSearchTool,
    SerperDevTool
)
from app import settings

app = FastAPI()

# Set API keys
os.environ["SERPER_API_KEY"] = str(settings.SERPER_API_KEY)
config = {"OPENAI_API_KEY": str(
    settings.OPENAI_API_KEY), "OPENAI_MODEL_NAME": "gpt-4-turbo"}

# Initialize the search tool
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Researcher
researcher = Agent(
    config=config,
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    )
)

# Agent 3: Resume Strategist
resume_strategist = Agent(
    config=config,
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market.",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    )
)

# Agent 4: Interview Preparer
interview_preparer = Agent(
    config=config,
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)

# Tasks
research_task = Task(
    description="Analyze the job posting and extract key requirements.",
    expected_output="A list of key job requirements and qualifications.",
    agent=researcher
)

profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub URLs and personal write-up. Utilize tools to "
        "extract and synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=researcher,
    async_execution=True
)

resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "including the initial summary, work experience, skills, "
        "and education. All to better reflect the candidate's "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    context=[research_task, profile_task],
    agent=resume_strategist
)

interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these questions and talking points to "
        "help the candidate highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)

# Create the crew
job_application_crew = Crew(
    agents=[researcher, resume_strategist, interview_preparer],
    tasks=[research_task, profile_task,
           resume_strategy_task, interview_preparation_task],
    verbose=True
)


@app.post("/process_resume/")
async def process_resume(
    github_url: str = Form(...),
    job_posting_url: str = Form(...),
    personal_writeup: str = Form(...),
    resume_file: UploadFile = File(...)
):
    # Save the uploaded resume to a temporary file
    resume_path = f"./{resume_file.filename}"
    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    # Update the tools that depend on the resume file
    read_resume = FileReadTool(file_path=resume_path)
    semantic_search_resume = MDXSearchTool(mdx=resume_path)
    resume_strategist.tools.extend([read_resume, semantic_search_resume])
    interview_preparer.tools.extend([read_resume, semantic_search_resume])

    # Update the task with the user's input
    job_application_inputs = {
        'job_posting_url': job_posting_url,
        'github_url': github_url,
        'personal_writeup': personal_writeup
    }

    # Kickoff the crew
    result = job_application_crew.kickoff(inputs=job_application_inputs)

    # Extract results
    research_results = research_task.output.raw_output if research_task.output else None
    profile_results = profile_task.output.raw_output if profile_task.output else None
    resume_results = resume_strategy_task.output.raw_output if resume_strategy_task.output else None
    interview_results = interview_preparation_task.output.raw_output if interview_preparation_task.output else None

    return {
        "research_results": research_results,
        "profile_results": profile_results,
        "resume_results": resume_results,
        "interview_results": interview_results
    }
