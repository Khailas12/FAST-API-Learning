from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

@app.get('/')   # path
def index():
    return {"data": "Hello"}


@app.get('/blog/{id}')
def blog(id: int):
    about = {"data": id}
    return about


@app.get('/blog/{id}/comments') # dynamic routing
def blog(id: int):
    about = {"data": {"comments": id}}
    return about

@app.get('/bloglist')
def blog_list(limit: int=10, published: bool = True, sort: Optional[str] = None):
    return {"data": f"{limit} is the Limit and {published} "}


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {"data": f"blog is being created with the {blog.title}"}



# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)    
