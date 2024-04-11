# this will be the root file where we create the fastapi application
from fastapi import Depends, HTTPException, Path, status, APIRouter
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from .auth import get_current_user

# create the app and connect it to the fastapi application
# Instead of using FASTapi as the app we use APIRouter instead as the app
# this comes with the FASTAPI module and helps with scalability
router = APIRouter(prefix="/admin", tags=["admin"])


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


# create a variable to hold the db dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed!")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("user.role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed!")
    todo_model = db.query(Todos).filter(Todos.todo_id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="To do not found!")
    db.query(Todos).filter(Todos.todo_id == todo_id).delete()
    db.commit()
