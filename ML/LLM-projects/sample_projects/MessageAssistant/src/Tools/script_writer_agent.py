import os
import json
from src.Tools import prompts


current_dir = os.path.dirname(__file__)
stm_dir = os.path.join(current_dir, '..', 'LTM/GrayMatter')


def press_release_prompt() -> str:
    """Return the prompt for the press release analysis."""
    return prompts.PRESS_RELEASE_ANALYSIS


def content_strategy_prompt() -> str:
    """Return the prompt for the content strategy suggestion."""
    return prompts.CONTENT_STRATEGY_SUGGESTION


def speech_writing() -> str:
    """Return the prompt for the content strategy suggestion."""
    return prompts.CONTENT_STRATEGY_SUGGESTION


def client_brief_prompt() -> str:
    """
    Return the prompt for the client brief clarification.
    import json from available_media.json, select relevant media outlets, add to the prompt
    """
    available_media = os.path.join(stm_dir, 'available_media.json')
    with open(available_media, "r") as f:
        media_outlets = json.load(f)
    media = media_outlets['Healthcare']
    modified_prompt = prompts.CLIENT_BRIEF_CLARIFICATION.replace('%media_outlets%', ", ".join(media))
    return modified_prompt


def none_case_catcher() -> str:
    """Return the prompt for the none case catcher."""
    prompt = """
            You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, ask the user for more clarification.
            Your response should start with a brief summary response and bullet points for details and explanations.
            Use three sentences maximum and keep the answer concise:

            {document}
            """
    return prompt


# print(client_brief_prompt())
