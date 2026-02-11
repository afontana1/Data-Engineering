# Fastchat Usage Examples 🧩

This document presents detailed use cases for the Fastchat project, designed to facilitate its integration and utilization in various scenarios. The main features are explained and practical examples are provided for each case, allowing users to understand the potential and flexibility of the tool.

## Simple Terminal Chat

The easiest way to interact with Fastchat is through the terminal. This method is ideal for quick tests, demos, or users who prefer the command line.

```python
from fastchat import TerminalChat

chat = TerminalChat()
chat.open()
```

Running this code starts an interactive chat session in the terminal. Users can send messages and receive real-time responses, with no additional configuration required.

## Using the Fastchat Module

For more advanced integration, it is recommended to use the `Fastchat` class. This approach allows you to incorporate Fastchat directly into Python applications, offering greater control over the conversation flow and asynchronous event management.

```python
from fastchat import Fastchat
import asyncio

async def chating():
    chat = Fastchat()
    await chat.initialize()
    while True:
        query = input("> ")
        if not query:
            break
        async for step in chat(query):
            print(f"<< {step.json}")

asyncio.run(chating())
```

In this example, a `Fastchat` instance is initialized and a conversation loop is maintained. Using `asyncio` enables efficient handling of multiple messages and leverages the module's asynchronous capabilities.

## Customizing System Prompts

Fastchat allows you to customize system prompts to tailor model responses to specific needs. This feature is useful when you require the assistant to follow particular instructions or maintain a certain context.

```python
from fastchat import Fastchat
import asyncio

async def chating():
    system_prompt_1 = "Respond as an artificial intelligence expert."
    system_prompt_2 = "Keep answers concise and technical."

    chat = Fastchat(
        extra_reponse_system_prompts=[
            system_prompt_1,
            system_prompt_2
        ]
    )

    await chat.initialize()
    # Rest of the conversation flow...

asyncio.run(chating())
```

The `extra_reponse_system_prompts` list lets you define multiple instructions that will be considered by the model in each interaction. This feature is available in the [`Fastchat`](../src/fastchat/app/chat/chat.py), [`TerminalChat`](../src/fastchat/local/local_chat.py), and [`Fastapp`](../src/fastchat/api/api.py) modules, making personalized configuration easy in any environment.

## Fastapp: REST API & WebSocket Exposure (Beta)

For applications requiring real-time communication or frontend integration, Fastchat offers the `Fastapp` module. This module enables you to create a REST API and a WebSocket, providing a robust interface to interact with the model from other systems.

```python
# my_api.py
from fastchat.api import Fastapp

fastapp = Fastapp(
    extra_reponse_system_prompts=[],
    extra_selection_system_prompts=[],
    len_context=ConfigLLM.DEFAULT_HISTORY_LEN,
)

app = fastapp.app
```

To start the server and expose the API, it is recommended to use `uvicorn`:

```shell
uvicorn my_api:app --host 0.0.0.0 --port 8000 --ws-ping-interval 0 --ws-ping-timeout 1200 --workers 1
```

This enables HTTP endpoints and a WebSocket at `/ws/chat`, allowing real-time interaction with the model. It is ideal for integration with web, mobile, or external systems. Currently, this functionality is in beta, and work is ongoing to implement authorization and security mechanisms.
