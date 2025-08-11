from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# How to connect to postgres
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost/discord_clone"

# Manages connection
engine = create_engine(DATABASE_URL)

# autoflush=Flase avoids auto write to database
# bind=engine sessions created by this maker uses engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():

    # Makes new database session
    db = SessionLocal

    try:

        # Gives session to endpoint handler
        # Using yield instead of return to tell fastapi to run the 
        # code afterwards
        yield db
    
    finally:
        db.close()