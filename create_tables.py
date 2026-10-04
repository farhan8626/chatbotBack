from app.database.database import engine
from app.models.chat import Base

print("Connecting to TiDB...")
# This command automatically reads your Python classes and builds the SQL tables
Base.metadata.create_all(bind=engine)