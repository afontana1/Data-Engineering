import os
from typing import List, Optional

import google.generativeai as genai

from .llm import LanguageModel, LLMOptions, Prompts


class GoogleLanguageModel(LanguageModel):
    def __init__(self, **opts: LLMOptions):
        super().__init__(**opts)
        self.client = genai.configure(
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )
        self.model = opts.get("model", "gemini-1.5-pro-latest")

    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        return super().chunk_text(text, chunk_size)

    def get_response_sync(self, prompts: Prompts) -> Optional[str]:
        """Calls the Google Gemini API with the provided prompt and returns the response."""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompts)
            return response.text  # type: ignore[no-any-return]
        except Exception as e:
            print(f"Error calling Google Gemini API: {e}")
        return None
