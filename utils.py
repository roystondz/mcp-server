import trafilatura # Used to extract text from HTML content
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

def clean_html_to_text(html: str) -> str:
    """
    Clean HTML content and return plain text.
    """
    try:
        extracted_text =  trafilatura.extract(
            html,
            favor_recall = False, # Maximise Precision (Remove irrelevent text) over completeness of the text
            output_format = "txt",
            include_comments = False,
            include_tables=False
        )
        if extracted_text:
            return extracted_text
        else:
            return "Unable to extract text from the provided HTML."
    except Exception as e:
        print("Error during text extraction:", e)
        return f"Error during text extraction: {str(e)}"

def get_response_from_llm(user_prompt, system_prompt, model):
    api_key = os.getenv("GROQ_API_KEY")

    groq = Groq(api_key=api_key)
    chat_completions = groq.chat.completions.create(
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_prompt}
        ],
        model = model
    )
    
    return chat_completions.choices[0].message.content

