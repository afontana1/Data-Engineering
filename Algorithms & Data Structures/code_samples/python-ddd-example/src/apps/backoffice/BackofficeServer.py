import uvicorn

from src.apps.backoffice.BackofficeApp import BackofficeApp
from src.contexts.shared.Infrastructure.environment.EnvManager import EnvManager
from src.contexts.shared.Infrastructure.environment.EnvVar import EnvVar


class BackofficeServer:

    def __init__(self):
        self.app = BackofficeApp()

    def run(self):
        host = EnvManager.get(EnvVar.BACKOFFICE_SERVER_HOST)
        port = EnvManager.get(EnvVar.BACKOFFICE_SERVER_PORT, parser=int)
        uvicorn.run(self.app.get_runnable(), host=host, port=port)
