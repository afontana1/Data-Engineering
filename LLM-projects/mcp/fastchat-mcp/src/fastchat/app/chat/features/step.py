from enum import Enum


class StepMessage(Enum):
    """
    Enum representing all available LLM processing steps.
    Each step includes a name and a clear description of its purpose.
    """

    ANALYZE_QUERY = (
        "analyze query",
        "Analyze the user query and available services to separate it into service-specific calls.",
    )

    SELECT_SERVICE = (
        "select service",
        "Select the most appropriate service for the current query.",
    )

    SELECT_PROMPTS = (
        "select prompts",
        "Select the mosts appropriates prompts for the current query and generate the necessary arguments for use with the selected prompts",
    )


class Step:
    def __init__(self, step_type: StepMessage, data: dict[str, any] | None = None):
        self.type: str = "step"
        self.step: str = step_type.value[0]
        self.message: str = step_type.value[1]
        self.data: dict[str, any] = data

        self.json: dict[str, any] = {
            "type": self.type,
            "step": self.step,
            "message": self.message,
            "data": self.data,
        }
        self.response: str | None = None
        self.query: str | None = None

    def __call__(self) -> dict:
        return self.json

    def __str__(self):
        result = f"\n### {self.step}\n{self.message}\n"
        if self.data is not None and len(self.data) > 0:
            # result += "#### Data\n"
            for key in self.data.keys():
                result += f"- **{key}:** {self.data[key]}\n"
        return result


class ResponseStep(Step):
    def __init__(
        self,
        response: str,
        data: dict[str, any] | None = None,
        first_chunk: bool = False,
        # last_chunk: bool = False,
    ):
        self.type: str = "response"
        self.response: str | None = (
            response if (response is not None and response != "None") else ""
        )
        self.data: dict[str, any] | None = data
        self.first_chunk: bool = first_chunk
        self.last_chunk: bool = data is not None

        self.json: dict[str, any] = {
            "type": self.type,
            "response": self.response,
            "data": data,
            "first_chunk": self.first_chunk,
        }

    def __str__(self):
        return (
            f"\n### Response\n{self.response}"
            if self.first_chunk
            else f"{self.response}"
        ) + (f"\n```json\n{self.data}\n```" if self.data is not None else "")


class QueryStep(Step):
    def __init__(self, query: str):
        self.type: str = "query"
        self.query: str | None = query
        self.json: dict[str, any] = {"type": self.type, "query": self.query}

    def __str__(self):
        return f"\n## {self.query}"


class DataStep(Step):
    def __init__(self, data: dict[str, any]):
        self.type: str = "data"
        self.data: dict[str, any] | None = data
        self.json: dict[str, any] = {"type": self.type, "data": self.data}

    def __str__(self):
        result = ""
        if self.data is not None and len(self.data) > 0:
            for key in self.data.keys():
                result += f"- **{key}:** {self.data[key]}\n"

        return result[:-1] if len(result) > 1 else result
