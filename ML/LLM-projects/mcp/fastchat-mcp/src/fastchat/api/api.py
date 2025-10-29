from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastauth import Fastauth, TokenRouter, FastauthSettings
from .settings import FastappSettings
from .routes.chat import router as chat_router
from ..config import ConfigLLM, AuthApiConfig
from ..utils.clear_console import clear_console


class FastApp:
    def __init__(
        self,
        extra_reponse_system_prompts: list[str] = [],
        extra_selection_system_prompts: list[str] = [],
        len_context: int = ConfigLLM.DEFAULT_HISTORY_LEN,
        token_router: TokenRouter = TokenRouter(),
        auth_settings: FastauthSettings | dict | None = AuthApiConfig().auth_settings,
    ):
        FastappSettings.update(
            extra_reponse_system_prompts,
            extra_selection_system_prompts,
            len_context,
        )

        
        auth_settings.access_token_paths += ["/chat/user"]
        auth_settings.master_token_paths += ["/chat/admin"]

        self.fastauth = Fastauth(settings=auth_settings)
        self.token_router = token_router

    @property
    def app(self) -> FastAPI:
        app: FastAPI = FastAPI()

        @app.get("/")
        async def root():
            return RedirectResponse(url="/docs")

        @app.get("/healt")
        async def healt():
            return {"status": "healtly"}

        app.include_router(chat_router)
        self.fastauth.set_auth(app, [self.token_router.route])
        return app

    def run(self, host: str, port: int):
        clear_console()
        pass
