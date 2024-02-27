from fastapi import FastAPI
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

from src.routes import photo, tags_routes, comments_routes, links_routes, auth_routes, user_routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(photo.router, prefix='/api')
app.include_router(tags_routes.router, prefix='/api')
app.include_router(comments_routes.router, prefix='/api')
app.include_router(links_routes.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "That's root"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000, reload=True)
    logging.basicConfig(level=logging.INFO)
