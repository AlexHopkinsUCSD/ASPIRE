from typing import Optional, List

from sqlmodel import Field, SQLModel, ForeignKey, Column, Integer

class ModuleBase(SQLModel):
    title: str = Field(max_length=255)
    domain_id: int = Field(foreign_key="domain.domain_id")
    content_summary: str

class ModuleBaseExtended(ModuleBase):
    module_id: Optional[int] = Field(default=None, primary_key=True)

class Module(ModuleBaseExtended, table=True):
    pass

class ModuleCreate(ModuleBase):
    course_id: int

class ModuleCreateNoLLM(SQLModel):
    title: str
    content_summary: str
    course_id: int

class ModuleRead(ModuleBaseExtended):
    pass

class ModuleUpdate(SQLModel):
    title: Optional[str] = None
    content_summary: Optional[str] = None


class ModuleToCourse(SQLModel, table=True):
    module_id: int = Field(foreign_key="module.module_id", primary_key=True)
    course_id: int = Field(sa_column=Column(Integer, ForeignKey(column="course.course_id", ondelete="CASCADE"), primary_key=True))

class ModuleConceptsResponse(SQLModel):

    concepts: List[str]

class ModuleSummary(SQLModel):
    summary: str