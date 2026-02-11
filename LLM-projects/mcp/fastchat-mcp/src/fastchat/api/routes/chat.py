import json
from fastauth import websocket_middleware, TokenType
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..settings import FastappSettings
from ...config.logger import logger
from ...app.chat.chat import Fastchat
from ...config.llm_config import ConfigGPT, ConfigLLM
from ...app.chat.features.llm_provider import LLMProvider

router = APIRouter(prefix="/chat", tags=["chating"])
STREAM_END_MARKER: str = "--eof"


@router.websocket("/user")
@websocket_middleware(token_type=TokenType.ACCESS)
async def access_websocket(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigGPT.DEFAULT_MODEL_NAME,
    llm_provider: str = ConfigLLM.DEFAULT_PROVIDER.value,
):
    await websocket_chat(
        websocket=websocket,
        chat_id=chat_id,
        model=model,
        llm_provider=llm_provider,
    )


@router.websocket("/admin")
@websocket_middleware(token_type=TokenType.MASTER)
async def master_websocket(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigGPT.DEFAULT_MODEL_NAME,
    llm_provider: str = ConfigLLM.DEFAULT_PROVIDER.value,
):
    await websocket_chat(
        websocket=websocket,
        chat_id=chat_id,
        model=model,
        llm_provider=llm_provider,
    )


async def websocket_chat(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigGPT.DEFAULT_MODEL_NAME,
    llm_provider: str = ConfigLLM.DEFAULT_PROVIDER.value,
):
    await websocket.accept()
    await websocket.send_json(
        {
            "status": "success",
            "detail": "Connected: Connection Accepted",
        }
    )
    aditional_servers: dict = websocket.headers.get("aditional_servers")
    if (
        aditional_servers is None
        or aditional_servers == ""
        or aditional_servers == "None"
    ):
        aditional_servers = {}
    else:
        try:
            aditional_servers = aditional_servers.replace("'", '"')
            aditional_servers = json.loads(aditional_servers)
        except:
            aditional_servers = {}

    llm_provider = LLMProvider(llm_provider)
    history: list = get_history(chat_id)

    chat = Fastchat(
        id=chat_id,
        model=model,
        llm_provider=llm_provider,
        extra_reponse_system_prompts=FastappSettings.extra_reponse_system_prompts,
        extra_selection_system_prompts=FastappSettings.extra_selection_system_prompts,
        aditional_servers=aditional_servers,
        len_context=FastappSettings.len_context,
        history=history,
    )

    logger.info(f"Initilaized chat with id = {chat_id}")
    await chat.initialize(print_logo=False)

    try:
        while True:
            # Espera mensaje del usuario, típicamente texto (puedes cambiarlo si envías JSON)
            query = await websocket.receive_text()
            response = chat(query)

            # Enviar respuesta al cliente (puede ser texto o JSON)
            async for step in response:
                await websocket.send_json(step.json)
            await websocket.send_text(STREAM_END_MARKER)

    except WebSocketDisconnect:
        # Cierra conexión limpia si el cliente se desconecta
        pass


def get_history(chat_id: str) -> list:
    """Select history from database using chat_id"""
    return []
