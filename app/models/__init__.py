from app.database.database import Base
from app.models.user import User, Role, Permission
from app.models.chat import Conversation, Message, Feedback
from app.models.knowledge import Category, Product, FAQ
from app.models.support import Ticket

# This file exposes all our models and the Base.
# This makes it very easy for Alembic (our migration tool) to discover all tables.
