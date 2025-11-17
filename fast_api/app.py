import asyncio
import platform
from http import HTTPStatus
from fastapi import FastAPI

from fast_api.API.v1.endpoints.auth_route import routh_auth
from fast_api.API.v1.endpoints.master_route import routh_master
from fast_api.API.v1.endpoints.Order_route import routh_order
from fast_api.API.v1.endpoints.users_route import routh_users
from fast_api.Schemas.Schema import Message


if platform.system() == "Windows":
    import sys
    if sys.version_info >= (3, 8) and sys.platform == "win32":
        from asyncio.windows_events import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
        print("Política de Event Loop do Windows aplicada com sucesso.")


app = FastAPI(title='E-commerce', version='1.0.0')

app.include_router(routh_auth)
app.include_router(routh_users)
app.include_router(routh_master)
app.include_router(routh_order)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def home():
    return {'message': 'E-commerce API no ar!'}

