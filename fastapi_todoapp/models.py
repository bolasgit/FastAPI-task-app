# models.py helps sqlalchemy understand what type of database tables we would create later
# it is the actual record that will be inside the database table
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey


class Users(Base):
    # the following code helps sqlalchemy to know what to name the table in the database later
    __tablename__ = "users"
    # Now we can build the columns
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Todos(Base):
    # the following code helps sqlalchemy to know what to name the table in the database later
    __tablename__ = "todos"
    # Now we can build the columns
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
