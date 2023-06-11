from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils.cache import redis_client


def start_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if redis_client.engine is not None:
            await redis_client.engine.close()

    server = FastAPI(title="Lexicom Test", lifespan=lifespan)

    from app.views.phone_numbers_address import router as phone_numbers_router

    server.include_router(phone_numbers_router, tags=['address_by_phone_number'])

    return server
