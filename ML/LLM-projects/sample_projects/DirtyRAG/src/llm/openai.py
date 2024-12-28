import os
from typing import List, Optional, cast

import openai
from openai import OpenAI

from .llm import EmbeddingOptions, LanguageModel, LLMOptions, Prompts


class OpenAILanguageModel(LanguageModel):
    def __init__(self, **opts: LLMOptions):
        super().__init__(**opts)
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        self.model: str = str(opts.get("model", "gpt-3.5-turbo"))  # Default model
        self.embedding_options: Optional[EmbeddingOptions] = cast(
            Optional[EmbeddingOptions], opts.get("embedding_params")
        )

    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        return super().chunk_text(text, chunk_size)

    def get_embedding(self, text: str) -> List[float]:
        if self.embedding_options is None:
            # TODO: Raise warning or throw error here instead of silent defaults
            self.embedding_options = {
                "dimensions": 1536,
                "model": "text-embedding-3-small",
            }

        response = openai.embeddings.create(
            input=text,
            dimensions=self.embedding_options.get("dimensions", 1536),
            model=self.embedding_options.get("model", "text-embedding-3-small"),
        )

        embedding = response
        if embedding.data is None or len(embedding.data) == 0:
            return []
        return embedding.data[0].embedding  # type: ignore

    def get_response_sync(
        self,
        messages: Prompts,
    ) -> Optional[str]:
        """Calls the OpenAI API with the provided prompt and returns the response."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )

            return chat_completion.choices[0].message.content  # type: ignore[no-any-return]
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
        return None
