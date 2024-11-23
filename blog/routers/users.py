from typing import List
from fastapi import APIRouter, Depends, status
from blog.database import get_db
from .. import schemas, oauth
from sqlalchemy.orm import Session
from ..repository import user_repo



router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return user_repo.create(user, db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return user_repo.get_all(db)


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return user_repo.get_one(id, db)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def update_user(id: int, user: schemas.ShowUser, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return user_repo.update(id, user, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_content(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return user_repo.delete(id, db)
