import redis.asyncio as redis

from backend.app.core.config import settings


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD
)

async def set_score(user_id: str, score: int):
    await r.set(f'user:{user_id}', score)

async def get_score(user_id: str) -> int:
    line = await r.get(f'user:{user_id}')
    return int(line) if line else None

async def update_score(user_id) -> int:
    score = await get_score(user_id)
    if score is None:
        score = 10
    else:
        score += 10
    await set_score(user_id, score)
    return score

async def delete_score(user_id: str):
    await r.delete(f'user:{user_id}')