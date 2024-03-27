# models.py helps sqlalchemy understand what type of database tables we would create later
# it is the actual record that will be inside the database table
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime


class Todos(Base):
    # the following code helps sqlalchemy to know what to name he table in the database later
    __tablename__ = "todos"
    # Now we can build the columns
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)


# class Users(Base):
#     # the following code helps sqlalchemy to know what to name he table in the database later
#     __tablename__ = "users"
#     # Now we can build the columns
#     user_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     phone_number = Column(Integer)
