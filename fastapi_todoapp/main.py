# this will be the root file where we create the fastapi application
from .routers import auth, todos, admin, users
from fastapi import FastAPI
from .database import engine

# import models
from .models import Base


# create the app and connect it to the fastapi application
app = FastAPI(title="SharpTodoApp", openapi_url="/api/v1/SharpTodoApp.html")

# creates everything in the database.py file and models.py file
# it then uses that to create as new database that has a new table called todos & columns in models.py
# all this without writing sql statements
Base.metadata.create_all(bind=engine)


@app.get("/healthy", tags=["Health"])
def health_check():
    return {"status": "Healthy"}


# include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# needed to edit the bcrypt file in fastapivenv as the error AttributeError: module 'bcrypt' has no attribute '__about__'
# kept stopping user authentication. Below is the path to the edited bcrypt file
# you may need to do the same if you directly install passlib and bcrypt
# "C:\impute\cdrive\path\to project\fastapi_apps\fastapivenv\lib\site-packages\passlib\handlers\bcrypt.py", line 620
