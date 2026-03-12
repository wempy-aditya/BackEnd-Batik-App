from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .admin.initialize import create_admin_interface
from .api import router
from .core.config import settings
from .core.setup import create_application, lifespan_factory

admin = create_admin_interface()


@asynccontextmanager
async def lifespan_with_admin(app: FastAPI) -> AsyncGenerator[None, None]:
    """Custom lifespan that includes admin initialization."""
    # Get the default lifespan
    default_lifespan = lifespan_factory(settings)

    # Run the default lifespan initialization and our admin initialization
    async with default_lifespan(app):
        # Initialize admin interface if it exists
        if admin:
            # Initialize admin database and setup
            await admin.initialize()

        yield


app = create_application(router=router, settings=settings, lifespan=lifespan_with_admin)

# Mount admin interface if enabled
if admin:
    app.mount(settings.CRUD_ADMIN_MOUNT_PATH, admin.app)

# Mount static files for uploads
import os
from pathlib import Path

# Try multiple possible upload directory locations
possible_upload_dirs = [
    os.getenv("UPLOADS_DIR", ""),
    "/app/uploads",
    "uploads",
    str(Path(__file__).parent.parent.parent / "uploads"),
]

uploads_dir = next((d for d in possible_upload_dirs if d and os.path.exists(d)), None)
if uploads_dir:
    app.mount("/api/v1/uploads", StaticFiles(directory=uploads_dir), name="uploads")
