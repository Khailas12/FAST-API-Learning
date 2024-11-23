from datetime import datetime
from fastapi import HTTPException, status
from .. import schemas, models
from sqlalchemy.orm import Session
from .. import hashing, utils



def login(email, password, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not hashing.pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Create JWT Token
    access_token = utils.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}