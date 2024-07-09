from typing import List, Optional, Protocol
from fastapi import UploadFile

from app.domain.models.forms import ModuleForm
from app.domain.models.module import ModuleRead, ModuleUpdate, ModuleCreateNoLLM
from app.domain.models.concept import ConceptRead


class ModuleService(Protocol):
    async def create_module(self, form_data: ModuleForm, files: List[UploadFile]) -> ModuleRead:
        ...

    async def create_module_no_llm(self, module: ModuleCreateNoLLM, concepts: Optional[List[ConceptRead]]) -> ModuleRead:
        ...

    async def get_module(self, module_id: int) -> ModuleRead:
        ...

    async def get_course_modules(self, course_id:int) -> List[ModuleRead]:
        ...

    async def get_domain_modules(self, domain_id: int) -> List[ModuleRead]:
        ...

    async def get_all_modules(self) -> List[ModuleRead]:
        ...

    async def update_module(self, module_id: int, module_update: ModuleUpdate) -> ModuleRead:
        ...

    async def delete_module_from_course(self, module_id: int, course_id: int) -> None:
        ...