from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blog, users, auth


app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blog.router)

