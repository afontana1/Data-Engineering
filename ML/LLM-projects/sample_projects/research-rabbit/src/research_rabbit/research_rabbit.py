import json

from typing_extensions import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph

from research_rabbit.configuration import Configuration
from research_rabbit.utils import deduplicate_and_format_sources, tavily_search, format_sources
from research_rabbit.state import SummaryState, SummaryStateInput, SummaryStateOutput
from research_rabbit.prompts import query_writer_instructions, summarizer_instructions, reflection_instructions

# LLM
llm = ChatOllama(model=Configuration.local_llm, temperature=0)
llm_json_mode = ChatOllama(model=Configuration.local_llm, temperature=0, format="json")

# Nodes   
def generate_query(state: SummaryState):
    """ Generate a query for web search """
    
    # Format the prompt
    query_writer_instructions_formatted = query_writer_instructions.format(research_topic=state.research_topic)

    # Generate a query
    result = llm_json_mode.invoke(
        [SystemMessage(content=query_writer_instructions_formatted),
        HumanMessage(content=f"Generate a query for web search:")]
    )   
    query = json.loads(result.content)
    
    return {"search_query": query['query']}

def web_research(state: SummaryState):
    """ Gather information from the web """
    
    # Search the web
    search_results = tavily_search(state.search_query, include_raw_content=True, max_results=1)
    
    # Format the sources
    search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
    return {"sources_gathered": [format_sources(search_results)], "research_loop_count": state.research_loop_count + 1, "web_research_results": [search_str]}

def summarize_sources(state: SummaryState):
    """ Summarize the gathered sources """
    
    # Existing summary
    existing_summary = state.running_summary

    # Most recent web research
    most_recent_web_research = state.web_research_results[-1]

    # Build the human message
    if existing_summary:
        human_message_content = (
            f"Extend the existing summary: {existing_summary}\n\n"
            f"Include new search results: {most_recent_web_research} "
            f"That addresses the following topic: {state.research_topic}"
        )
    else:
        human_message_content = (
            f"Generate a summary of these search results: {most_recent_web_research} "
            f"That addresses the following topic: {state.research_topic}"
        )

    # Run the LLM
    result = llm.invoke(
        [SystemMessage(content=summarizer_instructions),
        HumanMessage(content=human_message_content)]
    )

    running_summary = result.content
    return {"running_summary": running_summary}

def reflect_on_summary(state: SummaryState):
    """ Reflect on the summary and generate a follow-up query """

    # Generate a query
    result = llm_json_mode.invoke(
        [SystemMessage(content=reflection_instructions.format(research_topic=state.research_topic)),
        HumanMessage(content=f"Identify a knowledge gap and generate a follow-up web search query based on our existing knowledge: {state.running_summary}")]
    )   
    follow_up_query = json.loads(result.content)

    # Overwrite the search query
    return {"search_query": follow_up_query['follow_up_query']}

def finalize_summary(state: SummaryState):
    """ Finalize the summary """
    
    # Format all accumulated sources into a single bulleted list
    all_sources = "\n".join(source for source in state.sources_gathered)
    state.running_summary = f"## Summary\n\n{state.running_summary}\n\n ### Sources:\n{all_sources}"
    return {"running_summary": state.running_summary}

def route_research(state: SummaryState, config: RunnableConfig) -> Literal["finalize_summary", "web_research"]:
    """ Route the research based on the follow-up query """

    configurable = Configuration.from_runnable_config(config)
    if state.research_loop_count <= configurable.max_web_research_loops:
        return "web_research"
    else:
        return "finalize_summary" 
    
# Add nodes and edges 
builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput, config_schema=Configuration)
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", finalize_summary)

# Add edges
builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")
builder.add_conditional_edges("reflect_on_summary", route_research)
builder.add_edge("finalize_summary", END)

graph = builder.compile()