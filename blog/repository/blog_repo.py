from datetime import datetime
from fastapi import Depends, HTTPException, status

from blog import oauth
from .. import models, schemas
from sqlalchemy.orm import Session


def create(blog, db: Session, current_user):
    blog_exist = db.query(models.Blog).filter(models.Blog.title==blog.title).first()
    if blog_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog Title already exist"
    )
        
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_one(id, db: Session):
    blog = db.query(models.Blog).get(id)
    if not blog:
        detail = {"Error": f"Blog with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return blog

def update(id, blog_data: schemas.Blog, db: Session):
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


def delete(id, db: Session):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return "Delete Successful"
