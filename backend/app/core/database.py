from sqlmodel import SQLModel, create_engine, Session
import os

# Use absolute path to avoid "unable to open database file" errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Simplified path for Docker compatibility (writes to /app/production.db)
DB_Name = "production.db"
DB_PATH = os.path.join(os.getcwd(), DB_Name)
sqlite_url = f"sqlite:///{DB_PATH}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
