from typing import Optional, List, Union
from sqlmodel import Field, SQLModel, Column, VARCHAR

from .errors import DBError


class ConceptBase(SQLModel):
    name: str = Field(max_length=255, sa_column=Column("name", VARCHAR, unique=True, primary_key=True))

class ConceptBaseExtended(SQLModel):
    subject: str
    difficulty: int

class Concept(ConceptBase, ConceptBaseExtended, table=True):
    pass

class ConceptCreate(ConceptBase, ConceptBaseExtended):
    domain_id: int

class ConceptRead(ConceptBase):
    pass

class ConceptReadVerbose(ConceptBase, ConceptBaseExtended):
    pass

class ConceptCreateBulkRead(SQLModel):
    success: Union[List[ConceptRead], None]
    failed: Union[List[DBError], None]

class ConceptBulkRead(SQLModel):
    concepts: List[ConceptRead]

class ConceptFilter(SQLModel):
    course_id: Optional[int]
    subject: Optional[str]
    difficulty: Optional[int]

class ConceptFilterByCourse(SQLModel):
    course_id: int
    subject: bool=False
    difficulty: bool=False


class ConceptToConceptBase(SQLModel):
    concept_name: str = Field(foreign_key="concept.name", primary_key=True)
    prereq_name: str = Field(foreign_key="concept.name", primary_key=True)

class ConceptToConcept(ConceptToConceptBase, table=True):
    pass

class ConceptToConceptCreate(ConceptToConceptBase):
    pass

class ConceptToConceptRead(ConceptToConceptBase):
    pass

class ConceptToConceptDelete(ConceptToConceptBase):
    pass

class ConceptToDomainBase(SQLModel):
    concept_name: str = Field(foreign_key="concept.name", primary_key=True)
    domain_id: int = Field(foreign_key="domain.domain_id", primary_key=True)

class ConceptToDomain(ConceptToDomainBase, table=True):
    pass

class ConceptToDomainCreate(ConceptToDomainBase):
    pass

class ConceptToDomainRead(ConceptToDomainBase):
    pass


class ConceptToModuleBase(SQLModel):
    concept_name: str = Field(foreign_key="concept.name", primary_key=True)
    module_id: int = Field(foreign_key="module.module_id", primary_key=True)

class ConceptToModule(ConceptToModuleBase, table=True):
    pass

class ConceptToModuleCreate(ConceptToModuleBase):
    pass

class ConceptToModuleRead(ConceptToModuleBase):
    pass

class ConceptToModuleDelete(ConceptToModuleBase):
    pass