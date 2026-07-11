from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth import authentication
from db import models
from db.database import engine
from routers import posts, users

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


models.Base.metadata.create_all(engine)
app.mount("/images", StaticFiles(directory="images"), name="images")