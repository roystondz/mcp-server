from .utils import get_response_from_llm

def generate_llm_response(query, context, model="openai/gpt-oss-20b"):
    SYSTEM_PROMPT = """
    You are a helpful assistant that answers questions about libraries, tools, and general concepts.
    Answer only using the provided context. If info is missing say you dont know.
    Keep the 'SOURCE:' line exactly same to same.
    """

    USER_PROMPT = f"""
    Query: {query}
    Context: {context}
    """

    return get_response_from_llm(
        user_prompt=USER_PROMPT,
        system_prompt=SYSTEM_PROMPT,
        model=model
    )