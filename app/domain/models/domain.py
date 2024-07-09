from typing import Optional

from sqlmodel import Field, SQLModel

class DomainBase(SQLModel):
    domain_id: Optional[int] = Field(default=None, primary_key=True)

class DomainBaseExtended(DomainBase):
    name: str = Field(max_length=255)
    subject: str = Field(max_length=255)
    difficulty: int

class Domain(DomainBaseExtended, table=True):
    pass

class DomainCreate(DomainBaseExtended):
    pass

class DomainRead(DomainBase):
    pass

class DomainReadVerbose(DomainBaseExtended):
    pass