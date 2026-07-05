from fastapi import FastAPI
from db import models
from db.database import engine
from routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


models.Base.metadata.create_all(engine)
