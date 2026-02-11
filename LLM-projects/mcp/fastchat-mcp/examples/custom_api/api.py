from fastchat.api import FastApp
from fastauth import TokenRouter
from fastapi import FastAPI


class CustomTokenRouter(TokenRouter):
    def __generate_access_token(self, client_id):
        # Implement your custom logic here
        return super().__generate_access_token(client_id)

    def __refresh_access_token(self, refresh_token):
        # Implement your custom logic here
        return super().__refresh_access_token(refresh_token)


fastapp = FastApp(token_router=CustomTokenRouter())
app: FastAPI = fastapp.app

"""
To start the server and expose the API, it is recommended to use `uvicorn`:

```shell
uvicorn api:app --host 0.0.0.0 --port 8000 --ws-ping-interval 0 --ws-ping-timeout 1200 --workers 1
```

Modifica a guto el archivo [fastchat.config.json](fastchat.config.json)
"""