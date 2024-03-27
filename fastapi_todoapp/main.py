# this will be the root file where we create the fastapi application
from routers import auth, todos
from fastapi import FastAPI
from database import engine
import models


# create the app and connect it to the fastapi application
app = FastAPI()

# ask gpt to explain this code
# creates everything in the database.py file and models.py file
# it then uses that to create a new database that has a new table called todos & columns in models.py
# all this without writing sql statements
models.Base.metadata.create_all(bind=engine)

# include routers
app.include_router(auth.router)
app.include_router(todos.router)
