from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, status, HTTPException
from .database import engine, SessionLocal
from . import schemas, models, hashing
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.Blog, tags=['blog'])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.Blog], tags=['blog'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog, tags=['blog'])
def get_entity(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        detail = {"Error": f"Blog with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog, tags=['blog'])
def update_content(id: int, blog_data: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    
    blog_first = blog.first()
    if not blog_first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not found")

    # Prepare the data for update, adding the updated_at timestamp
    blog_data_dict = blog_data.model_dump()  
    blog_data_dict["updated_at"] = datetime.now() 
    
    blog.update(blog_data_dict, synchronize_session=False)
    
    db.commit()
    db.refresh(blog_first)
    return blog_first


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_content(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return "Delete Successful"


# User
@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['user'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.name==user.name or models.User.email==user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name or Email already registered"
        )
    
    pwd_hashing = hashing.Hasher.get_password_hash(user.password)
    new_user = models.User(name=user.name, email=user.email, password=pwd_hashing)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['user'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['user'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        detail = {"Error": f"user with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return user

@app.put('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['user'])
def update_user(id: int, user: schemas.ShowUser, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id==id)
    
    user_first = user_data.first()
    if not user_data:
        detail = {"Error": f"user with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    blog_data_dict = user.model_dump()  
    blog_data_dict["updated_at"] = datetime.now() 
    
    user_data.update(blog_data_dict, synchronize_session=False)
    
    db.commit()
    db.refresh(user_first)
    return user_first


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
def delete_content(id: int, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
    db.commit()
    return "Delete Successful"