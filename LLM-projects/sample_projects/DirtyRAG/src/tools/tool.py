from typing import Any, Dict, Protocol, TypedDict, TypeVar

from llm.llm import LanguageModel
from playwright_helper import PlaywrightHelper


class ContentPullOptions:
    pass


class ToolOptions(TypedDict, total=False):
    llm: LanguageModel
    source_params: Dict[str, Any]
    playwright: PlaywrightHelper


T = TypeVar("T", bound=ContentPullOptions, contravariant=True)


class Tool(Protocol):

    def __init__(self, **opts: ToolOptions): ...

    async def pull_content(self, opts: ToolOptions) -> str | Dict[str, Any]: ...

    def name(self) -> str: ...

    def get_prompts(self, prompt_helpers: Dict[str, Any]) -> Dict[str, str]: ...
