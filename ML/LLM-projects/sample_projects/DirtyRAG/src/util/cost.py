from typing import List, Optional

import pandas as pd
import tiktoken


# Helper func: calculate number of tokens
def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    if not string:
        return 0
    # Returns the number of tokens in a text string
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Helper function: calculate length of essay
def get_essay_length(essay: str) -> int:
    word_list: List[str] = essay.split()
    num_words: int = len(word_list)
    return num_words


# Helper function: calculate cost of embedding num_tokens
# Assumes we're using the text-embedding-ada-002 model
# See https://openai.com/pricing
def get_embedding_cost(num_tokens: int) -> float:
    return num_tokens / 1000 * 0.0001


# Helper function: calculate total cost of embedding all content in the dataframe
def get_total_embeddings_cost(df: pd.DataFrame) -> float:
    total_tokens: int = 0
    for i in range(len(df.index)):
        text: Optional[str] = df["content"][i]
        if text is not None:
            token_len: int = num_tokens_from_string(text)
            total_tokens += token_len
    total_cost: float = get_embedding_cost(total_tokens)
    return total_cost
