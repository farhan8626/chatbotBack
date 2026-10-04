import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# We expect a MySQL URL in the .env file like:
# mysql+pymysql://user:password@localhost:3306/quantan_db
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    connect_args={"ssl": {}} 
    # "mysql+pymysql://root:password@localhost:3306/quantan_db" # Fallback/Default
    # "mysql+mysqlconnector://2DhWaDab2Sziqqy.root:<PASSWORD>@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/sys" # Fallback/Default
#   " mysql+pymysql://4Sotxxejj9pN3Dx.root:eLatc68bmbvouP6P@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/sys"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # pool_pre_ping=True helps handle dropped connections gracefully
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency for FastAPI to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
