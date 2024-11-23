from typing import List
from fastapi import APIRouter, Depends, status
from blog.database import get_db
from .. import schemas, oauth
from sqlalchemy.orm import Session
from ..repository import blog_repo


router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return blog_repo.create(blog, db, current_user)


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return blog_repo.get_all(db)
    
@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_entity(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return blog_repo.get_one(id, db)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def update_content(id: int, blog_data: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return blog_repo.update(id, blog_data, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_content(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return blog_repo.delete(id, db)