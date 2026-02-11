import ast
import asyncio
import pprint

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# --- Configuration ---
SERVER_URL = "http://localhost:8000/mcp"  # adjust if hosted elsewhere

pp = pprint.PrettyPrinter(indent=2, width=100)


def unwrap_tool_result(resp):
    """
    Given a CallToolResult, return the Python object you actually want to iterate:
     - structured_content["result"] if present
     - otherwise try to parse resp.content as Python literal
     - otherwise return resp.content or resp itself
    """
    if hasattr(resp, "structured_content") and resp.structured_content:
        return resp.structured_content.get("result", resp.structured_content)
    if hasattr(resp, "content") and resp.content:
        text = resp.content
        try:
            return ast.literal_eval(text)
        except Exception:
            return text
    return resp


async def main():
    transport = StreamableHttpTransport(url=SERVER_URL)
    client = Client(transport)

    print("\n🚀 Connecting to FastMCP server at:", SERVER_URL)
    async with client:
        # 1. Ping
        print("\n🔗 Testing server connectivity...")
        await client.ping()
        print("✅ Server is reachable!\n")

        # 2. List what's available
        print("🛠️  Available tools:")
        tools = await client.list_tools()
        pp.pprint(tools)
        print()

        print("📚 Available resources:")
        resources = await client.list_resources()
        pp.pprint(resources)
        print()

        print("💬 Available prompts:")
        prompts = await client.list_prompts()
        pp.pprint(prompts)
        print()

        # 3. Fetch our AI topics resource
        print("\n📖 Fetching resource: resource://ai/arxiv_topics")
        try:
            res = await client.read_resource("resource://ai/arxiv_topics")
            text = res[0].text
            try:
                topics = ast.literal_eval(text)
            except Exception:
                topics = [text]
            print("Today's AI topics:")
            for i, t in enumerate(topics, 1):
                print(f"  {i}. {t}")
        except Exception as e:
            print(f"❌ Error fetching resource: {e}")
        print()

        # 4. Search Arxiv for a topic
        print("🔍 Testing tool: search_arxiv")
        try:
            raw = await client.call_tool(
                "search_arxiv",
                {"query": "Transformer interpretability", "max_results": 3},
            )
            search_results = unwrap_tool_result(raw)
            if not isinstance(search_results, list):
                raise ValueError("Expected a list of papers")
            for i, paper in enumerate(search_results, 1):
                print(f"  {i}. {paper['title']}\n     {paper['url']}")
        except Exception as e:
            print(f"❌ Error calling search_arxiv: {e}")
            search_results = []
        print()

        # 5. Summarize the first paper (if any)
        if search_results:
            first_url = search_results[0]["url"]
            print("📝 Testing tool: summarize_paper")
            try:
                raw = await client.call_tool(
                    "summarize_paper", {"paper_url": first_url}
                )
                summary = unwrap_tool_result(raw)
                print("\nSummary of first paper:\n", summary)
            except Exception as e:
                print(f"❌ Error calling summarize_paper: {e}")
            print()

        # 6. Generate the LLM prompt for a deep dive
        print("🚀 Testing prompt: explore_topic_prompt")
        try:
            prompt_resp = await client.get_prompt(
                "explore_topic_prompt", {"topic": "Transformer interpretability"}
            )
            print("\nGenerated prompt:")
            for msg in prompt_resp.messages:
                # use attributes instead of indexing
                print(f"{msg.role.upper()}: {msg.content}\n")
        except Exception as e:
            print(f"❌ Error calling prompt: {e}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
