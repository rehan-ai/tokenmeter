import tiktoken
from typing import Optional, List

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a given text for a specific model.
    
    :param text: The input text to count tokens for
    :param model: The model to use for token counting (default is gpt-3.5-turbo)
    :return: Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Warning: model '{model}' not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def truncate_text(text: str, max_tokens: int, model: str = "gpt-3.5-turbo") -> str:
    """
    Truncate text to fit within a specified token limit.
    
    :param text: The input text to truncate
    :param max_tokens: The maximum number of tokens allowed
    :param model: The model to use for token counting (default is gpt-3.5-turbo)
    :return: Truncated text
    """
    encoding = tiktoken.encoding_for_model(model)
    encoded = encoding.encode(text)
    
    if len(encoded) <= max_tokens:
        return text
    
    return encoding.decode(encoded[:max_tokens])

def split_text(text: str, chunk_size: int, model: str = "gpt-3.5-turbo") -> List[str]:
    """
    Split text into chunks of approximately equal token count.
    
    :param text: The input text to split
    :param chunk_size: The target size of each chunk in tokens
    :param model: The model to use for token counting (default is gpt-3.5-turbo)
    :return: List of text chunks
    """
    encoding = tiktoken.encoding_for_model(model)
    encoded = encoding.encode(text)
    chunks = []
    
    for i in range(0, len(encoded), chunk_size):
        chunk = encoding.decode(encoded[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# Usage example
if __name__ == "__main__":
    sample_text = "This is a sample text to demonstrate token counting and text manipulation utilities."
    
    token_count = count_tokens(sample_text)
    print(f"Token count: {token_count}")
    
    truncated_text = truncate_text(sample_text, 10)
    print(f"Truncated text: {truncated_text}")
    
    chunks = split_text(sample_text, 5)
    print("Text chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}")