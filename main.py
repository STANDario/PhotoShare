import redis.asyncio as redis
from fastapi import FastAPI
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.conf.config import settings
from src.routes import photo, tags, comments, links, auth, users


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(photo.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(links.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_domain,
                          port=settings.redis_port,
                          db=0,
                          encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "That's root"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000, reload=True)
    logging.basicConfig(level=logging.INFO)
