# we need a solution to scale main.py and auth.py to operate on the same port
# routers help us do that and APIRouter helps with that
# APIRouter helps us to have a main.py file the root of the application
# and on top of that seats other routes leading to different files with different apis and endpoints
# APIRouter allows us route from main.py file to auth.py file
from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}
