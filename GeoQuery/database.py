import os
from dotenv import load_dotenv
from sqlalchemy import create_engine



load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)