from fastapi import Depends, FastAPI, status, Response, HTTPException
from .database import engine, SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_201_CREATED)
def get_entity(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        detail = {"Error": f"Blog with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_200_OK)
def update_content(id: int, blog_data: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    blog_first = blog.first()
    if not blog_first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not found")

    blog.update(blog_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(blog_first)
    return blog_first


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_content(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return "Delete Successful"


