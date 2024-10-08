from typing import Optional, List, Annotated, Literal
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, ARRAY, Integer

class TriggerEventBase(SQLModel):
    datetime_stamp: datetime
    student_id: int = Field(foreign_key="student.student_id")
    concept: str = Field(foreign_key="concept.name")
    value: float
    weight: float

class TriggerEvent(TriggerEventBase, table=True):
    event_id: Optional[int] = Field(default=None, primary_key=True)

class TriggerEventCreate(TriggerEventBase):
    pass

class TriggerEventRead(TriggerEventBase):
    pass

class TriggerEventProcess(SQLModel):
    event_ids: list[float]
    concept: str = Field(foreign_key="concept.name")
    student_id: int = Field(foreign_key="student.student_id")
    numerator: float
    denominator: float