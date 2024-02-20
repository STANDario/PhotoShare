from fastapi import FastAPI
import uvicorn
import logging

from src.routes import post


app = FastAPI()


app.include_router(post.posts_router, prefix='/posts')


@app.get("/")
def read_root():
    return {"message": "That's root"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    logging.basicConfig(level=logging.INFO)
