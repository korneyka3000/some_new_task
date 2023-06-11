from fastapi import APIRouter, Depends, Response, status
from redis.asyncio.client import Redis

from utils.cache import conn_cache

from .schemas import PhoneAddress

router = APIRouter(tags=["address_by_phone_number"])


@router.get("/check_data")
async def read(
        phone: str,
        response: Response,
        redis: Redis = Depends(conn_cache)
):
    if address := await redis.get(phone):
        return {"address": address}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": f"No such phone_number: {phone}"}


@router.post("/write_data", status_code=status.HTTP_201_CREATED)
async def create(
        data: PhoneAddress,
        response: Response,
        redis: Redis = Depends(conn_cache)
):
    if await redis.exists(data.phone):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"error": f"already exists {data.phone}"}

    await redis.set(data.phone, data.address)
    return {"message": "created"}


@router.patch("/write_data")
async def patch(
        data: PhoneAddress,
        response: Response,
        redis: Redis = Depends(conn_cache)
):
    if not await redis.exists(data.phone):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"No such phone {data.phone}"}

    await redis.set(data.phone, data.address)
    return {"updated": f"{data.address}"}
