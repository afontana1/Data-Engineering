import asyncio
import os
import sys
from typing import Any, List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import newspaper
import psycopg2
import tiktoken
from dotenv import load_dotenv

from llm.openai import OpenAILanguageModel
from playwright_helper import PlaywrightHelper
from tools.google_search_tool import GoogleSearchOptions, GoogleSearchTool
from tools.tool import Tool

load_dotenv()

# Ensure the pgvector extension is enabled
connection_string = "postgresql://postgres:postgres@localhost:5001/ai"
conn = psycopg2.connect(connection_string)
cur = conn.cursor()

import concurrent.futures


async def main() -> None:
    async with PlaywrightHelper(launch_options={"headless": True}) as playwright_helper:
        query = input("> ")
        # language models
        openai_llm = OpenAILanguageModel()
        # googleai_llm = GoogleLanguageModel()

        googleSearchTool: Tool[GoogleSearchTool] = GoogleSearchTool(
            playwright=playwright_helper,
        )
        print(f"🧠 Searching {query.strip()}...")
        search_opts = GoogleSearchOptions()
        search_opts.query = query
        search_opts.sites = ["reddit.com"]

        links = await googleSearchTool.pull_content(search_opts)

        print("---------\n")
        print("Cleansing data...")
        cleansed_articles = parallelize_article_fetching(links)

        print("Parsing content...")
        for article in cleansed_articles:
            chunked_article = chunk_string(article.strip(), 512)
            for chunk in chunked_article:
                embedding = openai_llm.get_embedding(chunk)
                cur.execute(
                    """
                    INSERT INTO embeddings (text, embedding)
                    VALUES (%s, %s)
                """,
                    (chunk, embedding),
                )
                conn.commit()

        query_vector = openai_llm.get_embedding(query)
        cur.execute(
            """
            SELECT text, embedding
            FROM embeddings
            ORDER BY embedding <-> CAST(%s AS vector)
            LIMIT 5;
        """,
            (query_vector,),
        )

        results = cur.fetchall()
        context = []
        for row in results:
            text, embedding = row
            context.append(text)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful product recommendation engine who uses comments and feedback to determine the best products to buy.",
            },
            {
                "role": "user",
                "content": f"Find me the most recommended products based on what is inside 'context'. Ensure they are valid and accurate product names only. You can support telling me more than 1 product, but not more than 3. Tell me {query} given the following context: {' '.join(context)}. If the query isn't relevant to the context, just return the phrase 'I don't know'",
            },
            {
                "role": "user",
                "content": f"Make your response short and concise. Try your best to only return me the names and lists of recommended products and nothing else. Ensure all the product names are delimited by a comma like product 1, product 2",
            },
        ]
        print("Thinking...")
        print()
        result = openai_llm.get_response_sync(messages)
        results_and_links = []
        if result is not None:
            result = result.split(",")[:5]
            for buy_result in result:
                search_opts.query = buy_result
                search_opts.sites = None

                links = await googleSearchTool.pull_content(search_opts)
                if links is not None:
                    amazon_res = links["results"]
                    if amazon_res is None:
                        continue
                    results_and_links.append(
                        {"product": buy_result, "link": amazon_res}
                    )
                    print(f"Product: {amazon_res[0][0]}")
                    print(f"Link: {amazon_res[0][1]}")
                    print()

        cur.execute(
            """
        TRUNCATE embeddings;
        """.strip(),
        )
        conn.commit()


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    if not string:
        return 0
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def chunk_string(text: str, chunk_size: int) -> list[str]:
    words: list[str] = text.split()

    chunks: list[str] = []
    current_chunk: list[str] = []
    current_chunk_tokens: int = 0

    for word in words:
        word_tokens: int = num_tokens_from_string(word)
        if current_chunk_tokens + word_tokens > chunk_size:
            joined_chunk = " ".join(current_chunk)
            chunks.append(joined_chunk)
            current_chunk = []
            current_chunk_tokens = 0
        current_chunk.append(word)
        current_chunk_tokens += word_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def fetch_article(link: List[str]):
    article = newspaper.Article(url=link[1])
    article.download()
    article.parse()
    return article.text


def parallelize_article_fetching(links: Any, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_article, link) for link in links["results"][:5]
        ]
        cleansed_articles = [
            future.result() for future in concurrent.futures.as_completed(futures)
        ]
    return cleansed_articles


if __name__ == "__main__":
    asyncio.run(main())
