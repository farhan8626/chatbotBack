from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.router import api_router
from app.knowledge.loader import knowledge_base

from app.database.database import engine 
from app.models.chat import Base

# Initialize Rate Limiter (limits based on User IP)
limiter = Limiter(key_func=get_remote_address)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # This runs when the server starts up
#     print("Starting up Quantan AI Backend...")
#     knowledge_base.load_all()
#     yield
#     # This runs when the server shuts down
#     print("Shutting down Quantan AI Backend...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Quantan AI Backend...")
    
    # 1. Create all database tables if they do not exist
    Base.metadata.create_all(bind=engine)
    
    # 2. Load the RAG JSON files
    knowledge_base.load_all()
    yield
    print("Shutting down Quantan AI Backend...")

app = FastAPI(
    title="Quantan AI Support API",
    version="1.0.0",
    description="Backend API for Quantan AI Customer Support Chatbot",
    lifespan=lifespan
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for our frontend
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"], # Next.js dev server
    allow_origins=["https://chatbot-front-ecru.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Quantan AI Support API"}

@app.get("/health")
def health():
    return {"status": "healthy"}