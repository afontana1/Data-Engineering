# Database Connection

This document describes how to configure and interact with external database endpoints within the Fastchat MCP project. By specifying connection details in the configuration file, Fastchat can seamlessly store and retrieve chat data through HTTP endpoints.

## Configuration Structure

Database connection settings are defined in the `config.file`. If the connection is established successfully, the conversation flow will automatically handle sending and retrieving data from the specified endpoints.

```json
{
    "...": "...",

    "db_conection": {
        "root_path": "http://127.0.0.1:6543/fastchatdb",
        "headers": {
            "example_autorization_token": "<your_token_here>",
            "other_header": "value",
            "...": "..."
        },
        "base_body": {
            "company_id": "<your_company_id>",
            "example_body_param": "<your_value_here>",
            "other_body_param": "value",
            "...": "..."
        },
        "base_query": {
            "company_id": "<your_company_id>",
            "example_query_param": "<your_value_here>",
            "other_query_param": "value",
            "...": "..."
        },
        "endpoints": {
            "save_message": {
                "path": "/message/save"
            },
            "load_history": {
                "path": "/history/load"
            }
        }
    }
}
```

[See config.example](../fastchat.config.example.json)

## Data Sent to Each Endpoint

Each endpoint receives the data described below, in addition to the parameters provided in the `.config.json` file. For POST requests, the `"base_body"` is merged with endpoint-specific data. For GET requests, the `"base_query"` is used in a similar manner.

[See source code](../src/fastchat/app/client_db/client_db.py)

### Base endpoints path

```python
# base endpoints path
ROOT_PATH = "http://127.0.0.1:6543/fastchatdb/"
SAVE_HISTORY = "history/save"
SAVE_MESSAGE = "message/save"
LOAD_HISTORY = "history/load"
```

### Load History (GET)

The `load_history` endpoint is accessed via a GET request, passing the `chat_id` as a query parameter to retrieve the chat history.

```python
# load history function
def load_history(self, chat_id: str) -> list:
    """
    Load the chat history from the database via the configured endpoint.
    Returns the history as a list if successful, otherwise an empty list.
    """
    ...
```

### Save Message (POST)

The `save_message` endpoint receives the `chat_id` associated with the chat, the `message_id` of the message to be saved, and the message information as a dictionary.

```python
# save message function
async def save_message(
        self,
        chat_id: str,
        message_id: str,
        message: MessagesSet,
    ) -> bool:
    """
    Asynchronously save a single message to the database via the configured endpoint. Returns True if the operation was successful.
    """
    ...
```

### Message Information Structure (`MessageSet.info`)

Each message is structured as follows:

```json
{
    "id": "2e68583d-185d-4a84-a1cb-b156bf354810",
    "history": [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hello! I’m here to help with MCP services. At the moment, there are no MCP services configured in this context. \n\nIf you intended to connect to a service, please provide:\n- the service name (or ID),\n- or the configuration/details needed to establish the connection.\n\nI can then help with:\n- diagnosing issues and interpreting states or errors,\n- performing common MCP tasks (status checks, data reads/writes, event publishing, subscriptions, configuration changes),\n- guiding you through setup or troubleshooting steps.\n\nTell me what you’d like to do."
        }
    ],
    "flow": [
        {
            "query": "Hello"
        },
        {
            "selected_querys": [
                "Hello"
            ]
        },
        {
            "llm_message": {
                "role": "user",
                "content": "Hello"
            }
        },
        {
            "selected_prompts": []
        },
        {
            "selected_service": {
                "service": "",
                "args": {}
            }
        },
        {
            "llm_message": {
                "role": "assistant",
                "content": "Hello! I’m here to help with MCP services. At the moment, there are no MCP services configured in this context. \n\nIf you intended to connect to a service, please provide:\n- the service name (or ID),\n- or the configuration/details needed to establish the connection.\n\nI can then help with:\n- diagnosing issues and interpreting states or errors,\n- performing common MCP tasks (status checks, data reads/writes, event publishing, subscriptions, configuration changes),\n- guiding you through setup or troubleshooting steps.\n\nTell me what you’d like to do."
            }
        }
    ]
}
```

## Data Handling Workflow

- When a `Fastchat()` instance is created with a chat ID, it attempts to load the chat history from the `load_history` endpoint.
- After each conversation query, once a response is generated, a POST request is sent to the `save_message` endpoint to persist the latest message details.
