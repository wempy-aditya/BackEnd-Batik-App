"""
Public API endpoints
Frontend/Homepage endpoints - No authentication required
"""

from fastapi import APIRouter

from .ai_models import router as ai_models_router
from .categories import router as categories_router
from .datasets import router as datasets_router
from .gallery import router as gallery_router
from .news import router as news_router
from .projects import router as projects_router
from .publications import router as publications_router

router = APIRouter()

# Register all public endpoint routers
router.include_router(projects_router, prefix="/projects", tags=["Public - Projects"])
router.include_router(datasets_router, prefix="/datasets", tags=["Public - Datasets"])
router.include_router(ai_models_router, prefix="/ai-models", tags=["Public - AI Models"])
router.include_router(publications_router, prefix="/publications", tags=["Public - Publications"])
router.include_router(news_router, prefix="/news", tags=["Public - News"])
router.include_router(gallery_router, prefix="/gallery", tags=["Public - Gallery"])
router.include_router(categories_router, prefix="/categories", tags=["Public - Categories"])
