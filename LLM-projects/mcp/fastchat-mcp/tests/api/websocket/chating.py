"""
## WIKI
Crear uri pasando cada uno de los parametros deseados por parametros:
- chat_id: str
- model: str
- llm_provider: str
- len_context: int

```python
uri_ws = "ws://localhost:8000/chat/ws?chat_id=<your-chat-id>&model=<your_model-name>&llm_provider=<your-provider>&len_contex=<your-len-contex>"
```

> Para mas detalles ver documentacion de Fastchat en src/fastchat/app/chat/chat.py

__En caso de no pasar uno de estos valores, entonces se usara el valor por defecto__
"""

import asyncio
import websockets
from fastchat.utils.clear_console import clear_console
from fastchat.config.logger import LoggerFeatures, CustomFormatter
import json


class WebsocketClient:
    def __init__(self):
        pass

    def open_chat(self, uri, aditional_servers=None):
        clear_console()
        print(LoggerFeatures.LOGO + CustomFormatter.reset)
        asyncio.run(self.__open_chat(uri, aditional_servers))

    async def __open_chat(self, uri, aditional_servers):
        headers = {
            "aditional_servers": aditional_servers,
            "ACCESS-TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiI3NzAxODUyYi0xYmEzLTQ2NjQtYTJiYS1iYzBkMDBmMWExNGQiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTg4NDUyLCJpYXQiOjE3NTYzOTY0NTJ9.VLZVTK0SfM01pdg7XSy3dfAnO7-udarwDbCr8ImtdN4",
            "MASTER-TOKEN": "oBd-k41TmMqib1QYalke7HRCbk_HOtE0nw1YcdkibPc=",
        }

        async with websockets.connect(
            uri, additional_headers=headers, ping_interval=0
        ) as websocket:
            connection = await websocket.recv()
            connection = json.loads(connection)
            accepted: bool = connection["status"] == "success"
            print(("✅" if accepted else "❌") + f" {connection['detail']}\n")

            while accepted:
                mensaje = input(">> ")  # Leer mensaje a enviar desde consola
                await websocket.send(mensaje)  # Enviar mensaje al servidor

                # Esperar y recibir una o varias respuestas JSON en cadena (puedes adaptarlo según tu protocolo)
                try:
                    index = 1
                    while True:
                        step = await websocket.recv()
                        if step == "--eof":
                            break
                        step = json.loads(step)
                        index = step2terminal(step, index)
                except asyncio.TimeoutError:
                    pass


def step2terminal(step: dict, index: int) -> int:
    if step["type"] == "response":
        if step["first_chunk"]:
            print(f"<< {step['response']}", end="")
        else:
            print(f"{step['response']}", end="")
    if step["type"] == "query":
        print(f">> {step['query']}")
        _index = 1
    if step["type"] == "data":
        print(f"   {step['data']}")
    if step["type"] == "step":
        print(f"  {index}. {step['step']}")
        _index = index + 1

    return index


if __name__ == "__main__":
    uri_ws = "ws://localhost:8000/chat/user?chat_id=id" 
    uri_ws = "ws://localhost:8000/chat/admin?chat_id=id" 
    WebsocketClient().open_chat(uri_ws)
