import tiktoken

def count_tokens(text: str) -> int:
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = tokenizer.encode(text)
    return len(tokens)

conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
]

total_tokens = 0
for message in conversation:
    total_tokens += count_tokens(message["content"])

print(f"Total tokens in the conversation: {total_tokens}")