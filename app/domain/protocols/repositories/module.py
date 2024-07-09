from typing import Protocol, Literal, Optional, List

from app.domain.models.module import ModuleCreate, ModuleRead, ModuleUpdate


class ModuleRepository(Protocol):
    async def add(self, module: ModuleCreate) -> ModuleRead:
        ...

    async def get_one(self, module_id: int) -> ModuleRead:
        ...
    
    async def get_all(self, filter_name: Literal["course", "domain", "all"], filter_id: Optional[int]) -> List[ModuleRead]:
        ...
    
    async def update(self, module_id: int, module_update: ModuleUpdate) -> ModuleRead:
        ...

    async def delete_from_course(self, module_id: int, course_id: int) -> None:
        ...