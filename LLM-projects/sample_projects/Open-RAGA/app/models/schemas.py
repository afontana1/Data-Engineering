from pydantic import BaseModel,model_validator
from typing import List
from typing_extensions import Self


class ChatInput(BaseModel):

    query: str
    last_3_turn: List[dict]


    @model_validator(mode='wrap')
    def validate_chat_input(cls, values, handler):
        # This calls the default validation (e.g., type conversion)
        validated = handler(values)

        # ✅ Validate 'query'
        if not isinstance(validated.query, str) or not validated.query.strip():
            raise ValueError("query must be a non-empty string")

        # Check if length greater > 6
        if len(validated.last_3_turn) > 6:
            raise ValueError("last_3_turn must have  < 6 items")

        # Check if length greater > 6
        if len(validated.query.strip()) > 200:
            raise ValueError("query character length exceeds")

        # Check for all content should be dictionary
        if not all(isinstance(item, dict) for item in validated.last_3_turn):
            raise ValueError("Each item in last_3_turn must be a dictionary")

        return validated





class ChatOutput(BaseModel):

    response: str

    @model_validator(mode='before')
    def check_response(cls, values):

        if not isinstance(values.get('response'),str) or not values.get('response').strip():

            raise ValueError("query must be a non-empty string")

        return  values




class HistoryItem(BaseModel):
    human: str
    ai: str
