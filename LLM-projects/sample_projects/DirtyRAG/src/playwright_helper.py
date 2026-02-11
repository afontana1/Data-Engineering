from types import TracebackType
from typing import Dict, List, Optional, Type, TypedDict, Union

from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async


class LaunchOptions(TypedDict, total=False):
    headless: bool
    slow_mo: int
    devtools: bool
    timeout: float
    ignore_default_args: Union[bool, List[str]]
    args: List[str]
    proxy: Optional[Dict[str, str]]
    downloads_path: str
    chromium_sandbox: bool
    firefox_user_prefs: Dict[str, Union[str, int, bool]]


class PlaywrightHelper:
    # browser: Optional[Browser] = None
    # playwright: Optional[Playwright] = None
    # launch_options: Optional[LaunchOptions] = None

    async def __aenter__(self) -> "PlaywrightHelper":
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.browser:
            await self.browser.close()

    async def initialize(self) -> None:
        pass

    def __init__(self, launch_options: Optional[LaunchOptions] = None) -> None:
        self.browser: Optional[Browser] = None
        self.ctx: Optional[BrowserContext] = None
        self.playwright: Optional[Playwright] = None
        self.launch_options: Optional[LaunchOptions] = launch_options

    async def launch_browser(
        self,
        browser_type: Optional[BrowserType] = None,
    ) -> Browser:
        self.playwright = await async_playwright().start()
        try:
            if browser_type is None:
                browser_type = self.playwright.chromium

            headless: Optional[bool] = False
            if self.launch_options is not None:
                headless = self.launch_options.get("headless", False)

            browser = await browser_type.launch(headless=headless)
            if browser is None:
                raise Exception("Invalid browser instance")

            self.ctx = await browser.new_context()
            self.browser = browser
            return browser
        except Exception as e:
            print(f"An error occurred while launching the browser: {e}")
            raise

    async def get_context(self) -> BrowserContext:
        if self.browser is None:
            raise Exception("Browser has not been launched")
        if self.ctx is None:
            self.ctx = await self.browser.new_context()
        return self.ctx

    async def get_page(self) -> Page:
        if self.browser is None:
            await self.launch_browser()
        if self.ctx is None:
            await self.get_context()

        if self.ctx is not None:
            stealth_page = await self.ctx.new_page()
            await stealth_async(stealth_page)
            return stealth_page

        raise Exception("Conext was missing")

    async def get_stealth_page(self) -> Page:
        if self.browser is None:
            await self.launch_browser()
        if self.ctx is None:
            await self.get_context()

        if self.ctx is not None:
            return await self.ctx.new_page()

        raise Exception("Conext was missing")

    async def get_html_body(self, url: str, page: Page) -> str:
        await page.goto(url)
        await page.wait_for_selector("body")
        return await page.content()

    async def take_screenshot(self, page: Page, output_path="debug_img/screenshot.png"):
        await page.screenshot(path=output_path)

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
