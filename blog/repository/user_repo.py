from datetime import datetime
from fastapi import HTTPException, status
from blog import schemas, models
from sqlalchemy.orm import Session
from blog import hashing


def create(user, db:Session):
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


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get_one(id, db: Session):
    user = db.query(models.User).get(id)
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        detail = {"Error": f"user with {id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return user


def update(id, user: schemas.ShowUser, db: Session):
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


def delete(id, db: Session):
    db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
    db.commit()
    return "Delete Successful"
