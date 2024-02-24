from fastapi import FastAPI
import uvicorn
import logging

from src.routes import photo


app = FastAPI()


app.include_router(photo.router, prefix='/photo')


@app.get("/")
def read_root():
    return {"message": "That's root"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000, reload=True)
    logging.basicConfig(level=logging.INFO)