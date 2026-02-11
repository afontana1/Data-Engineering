import uuid


class MessagesSet:
    def __init__(self, query: str):
        self.root_query: str = query
        self.id: str = str(uuid.uuid4())

        self.history_messages: list[dict] = []
        self.flow_messages: list[dict] = [{"query": query}]

    def append_message(self, message: dict):
        self.history_messages.append(message)
        self.flow_messages.append({"llm_message": message})

    def selected_prompts(self, prompts: list[dict]):
        self.flow_messages.append({"selected_prompts": prompts})

    def selected_service(self, service: dict):
        self.flow_messages.append({"selected_service": service})

    def selected_querys(self, querys: list[str]):
        self.flow_messages.append({"selected_querys": querys})

    @property
    def info(self) -> dict:
        return {
            "id": self.id,
            "history": self.history_messages,
            "flow": self.flow_messages,
        }