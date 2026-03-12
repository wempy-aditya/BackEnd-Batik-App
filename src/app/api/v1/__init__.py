from fastapi import APIRouter

from .dashboard import router as dashboard_router
from .endpoints.ai_models import router as ai_models_router
from .endpoints.categories import router as categories_router
from .endpoints.contributors import router as contributors_router
from .endpoints.datasets import router as datasets_router
from .endpoints.files import router as files_router
from .endpoints.gallery import router as gallery_router
from .endpoints.news import router as news_router

# Admin/Protected content endpoints
from .endpoints.projects import router as projects_router
from .endpoints.publications import router as publications_router
from .health import router as health_router
from .login import router as login_router
from .logout import router as logout_router
from .posts import router as posts_router

# Public/Frontend endpoints (no auth required)
from .public import router as public_router
from .rate_limits import router as rate_limits_router
from .tasks import router as tasks_router
from .tiers import router as tiers_router
from .users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(dashboard_router)
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(tasks_router)
router.include_router(tiers_router)
router.include_router(rate_limits_router)

# Include admin/protected content routers
router.include_router(projects_router, prefix="/projects", tags=["projects"])
router.include_router(datasets_router, prefix="/datasets", tags=["datasets"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(publications_router, prefix="/publications", tags=["publications"])
router.include_router(news_router, prefix="/news", tags=["news"])
router.include_router(ai_models_router, prefix="/ai-models", tags=["ai-models"])
router.include_router(gallery_router, prefix="/gallery", tags=["gallery"])
router.include_router(contributors_router, prefix="/contributors", tags=["contributors"])
router.include_router(files_router)

# Include public/frontend routers (no authentication required)
router.include_router(public_router, prefix="/public")
