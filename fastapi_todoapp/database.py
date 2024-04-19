from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# url to create a location of database on the fastapi application
# database will be inside the directory of the todo application
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos_app.db"


# connect to mysql server
# pip install pymysql
# SQLALCHEMY_DATABASE_URL = ("mysql+pymysql://root:db_password@127.0.0.1:3306/todoapplicationdatabase")

# connect to postgresql server
# pip install psycopg2-binary to connect to postgres database
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:db_password@localhost/TodoApplicationDatabase"
)

# engine is used to open up connection and use database
# connect args are used to define a connection to database
# use the following engine for sqlite database
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# use the following engine for postgres and mysql database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session local-- create instance of the session local that will become a database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a database object we can interact with later
# we want to be able to call our database.py and create a base -
# object of the database to control the database
Base = declarative_base()
