from typing import Optional, List, Literal
from datetime import date
from enum import Enum

from pydantic import BaseModel

from sqlmodel import Field, SQLModel, Column, ARRAY, Integer


class CourseBase(SQLModel):
    course_id: Optional[int] = Field(default=None, primary_key=True)
    domain_id: int = Field(foreign_key="domain.domain_id")

class CourseBaseExtended(CourseBase):
    name: str = Field(max_length=255)
    quarter: date
    instructor: str
    course_summary: Optional[str] = None

class CourseBaseFull(CourseBaseExtended):
    user_ids: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(Integer())))

class Course(CourseBaseFull, table=True):
    pass

class CoursePreCreate(CourseBaseExtended):
    pass

class CourseCreate(CourseBaseFull):
    pass

class CourseCreateAPI(SQLModel):
    domain_id: int
    name: str
    quarter: date
    instructor: str
    course_summary: str

class CourseRead(CourseBase):
    pass

class CourseReadVerbose(CourseBaseExtended):
    pass

class CourseFilter(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    quarter: Optional[date] = None
    quarter_filter: Optional[Literal["equal", "newer", "older", "newer-inclusive", "older-inclusive"]] = None
    subject: Optional[str] = None
    difficulty: Optional[int] = None

class CourseUpdate(SQLModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    quarter: Optional[date] = None
    course_summary: Optional[str] = None
