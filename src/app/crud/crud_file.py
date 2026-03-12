"""
CRUD operations for File model using FastCRUD
"""

from typing import Optional
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.file import File


class CRUDFile(FastCRUD):
    def __init__(self):
        super().__init__(File)

    async def get_by_filename(self, db: AsyncSession, filename: str) -> dict | None:
        """Get file by filename"""
        return await self.get(db=db, filename=filename)

    async def get_files_by_type(self, db: AsyncSession, file_type: str, offset: int = 0, limit: int = 50) -> dict:
        """Get files filtered by type"""
        return await self.get_multi(db=db, offset=offset, limit=limit, file_type=file_type)

    async def get_files_by_user(self, db: AsyncSession, user_id: UUID, offset: int = 0, limit: int = 50) -> dict:
        """Get files uploaded by specific user"""
        return await self.get_multi(db=db, offset=offset, limit=limit, uploaded_by=user_id)

    async def get_total_storage_size(self, db: AsyncSession, user_id: Optional[UUID] = None) -> int:
        """Get total storage size used (in bytes)"""
        query = select(func.sum(File.file_size))

        if user_id:
            query = query.where(File.uploaded_by == user_id)

        result = await db.execute(query)
        total = result.scalar()

        return total or 0

    async def search_files(self, db: AsyncSession, search: str, offset: int = 0, limit: int = 50) -> dict:
        """Search files by original filename"""
        return await self.get_multi(db=db, offset=offset, limit=limit, original_filename__icontains=search)


# Create instance
crud_file = CRUDFile()
