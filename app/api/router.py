from fastapi import APIRouter

# Import individual endpoint routers (we will create these as we go)
from app.api import auth, chat, admin
# from app.api import products, faq

api_router = APIRouter()

# Registering routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# api_router.include_router(products.router, prefix="/products", tags=["Products"])
# api_router.include_router(faq.router, prefix="/faq", tags=["FAQ"])
# api_router.include_router(products.router, prefix="/products", tags=["Products"])
# api_router.include_router(faq.router, prefix="/faq", tags=["FAQ"])
# api_router.include_router(products.router, prefix="/products", tags=["Products"])
# api_router.include_router(faq.router, prefix="/faq", tags=["FAQ"])
