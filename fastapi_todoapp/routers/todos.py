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
router = APIRouter()


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


# create a class for the request model
# create a pydantic request or todo request post http request with body of a todo
class TodoRequest(BaseModel):
    # sqlalchemy covers the task_id and auto updates the id since it is the primary key
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=300)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# create asynchronous fastapi application
# depends is a dependency injection that means we need to do something before doing another thing
# We use it here to inject the dependencies that the function relies on
# the session relies on the get_db being able to open up a session and return info and closing session
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()


# refactors all "@app" to "@router" so they can run in this routers folder and accessed in main.py
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    # create a model to query the database just like a sql query
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.task_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


# cd in terminal to proper folder and use uvicorn main:app --reload to load the fastapi app to test


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("user_id"))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.task_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="To do not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed!")
    todo_model = (
        db.query(Todos)
        .filter(Todos.task_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status=404, detail="Task not found!")
    db.query(Todos).filter(Todos.task_id == todo_id).filter(
        Todos.owner_id == user.get("user_id")
    ).delete()
    db.commit()
