from fastapi import Depends, HTTPException, Path, status, APIRouter
from pydantic import BaseModel, Field
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Users
from .auth import get_current_user
from passlib.context import CryptContext

# create the app and connect it to the fastapi application
# Instead of using FASTapi as the app we use APIRouter instead as the app
# this comes with the FASTAPI module and helps with scalability
router = APIRouter(prefix="/users", tags=["Users"])


# ----------------------------------------------------------------
# to run sqlite3 cd to todos app and run sqlite3 "database_name.db" to mimic the database created
# use .schema to check db schema, "insert into database to create entries"
# use .mode table to change viz on terminal
# ----------------------------------------------------------------


# yield means only the code prior to and including the yield statement is executed before sending response
# then close the connection
# finally will run after the response has been delivered
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UserPhoneNumber(BaseModel):
    new_phone_number: str = Field(min_length=6)


# create a variable to hold the db dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed!")
    user = db.query(Users).filter(Users.user_id == user.get("user_id")).first()
    return user


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.user_id == user.get("user_id")).first()
    if bcrypt_context.verify(
        user_model.hashed_password, bcrypt_context.hash(user_verification.new_password)
    ):
        raise HTTPException(status_code=401, detail="Error on password change!")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: user_dependency, db: db_dependency, user_phone_number: UserPhoneNumber
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.user_id == user.get("user_id")).first()
    user_model.phone_number = user_phone_number.new_phone_number

    db.add(user_model)
    db.commit()
