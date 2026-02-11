from typing import Any, Dict, List, Optional, TypedDict

from playwright_helper import PlaywrightHelper

from .tool import ContentPullOptions, Tool, ToolOptions


class GoogleSearchOptions(ContentPullOptions):
    query: Optional[str]
    sites: Optional[List[str]]


class GoogleSearchResult(TypedDict, total=False):
    title: str
    link: str


class GoogleSearchTool(Tool):
    def __init__(self, **opts: ToolOptions):
        playwright: Optional[PlaywrightHelper] = opts.get("playwright")
        if playwright == None:
            raise Exception(f"Missing PlaywrightHelper instance")
        self.playwright: PlaywrightHelper = playwright

    async def get_html(self, query: str) -> str:
        page = await self.playwright.get_stealth_page()
        await page.goto(query)
        await page.wait_for_load_state("networkidle")
        contents = await page.content()
        return str(contents)

    async def pull_content(
        self,
        opts: ToolOptions,
    ) -> str | Dict[str, Any]:
        query = ""
        if not isinstance(opts, GoogleSearchOptions):
            raise Exception("Invalid options provided.")

        if opts.query is None:
            raise Exception("Missing search query")

        query = opts.query
        query = query.replace(" ", "+")

        page = await self.playwright.get_stealth_page()
        search_url = (
            f"https://www.google.com/search?hl=en&source=hp&biw=&bih=&q={query}"
        )

        sites = ""
        if opts.sites is not None:
            for url in opts.sites:
                sites = f"{sites} site:{url}"
        search_url = f"{search_url}{sites}"
        await page.goto(search_url)

        await page.wait_for_load_state("networkidle")
        elements = await page.query_selector_all("span > a > h3")
        results = []
        if elements:
            for _, element in enumerate(elements):
                a_tag = await element.query_selector("xpath=..")

                if a_tag is not None:
                    href = await a_tag.get_attribute("href")
                    results.append([await element.text_content(), href])
        return {"results": results}

    def name(self) -> str:
        return "Google Search"
