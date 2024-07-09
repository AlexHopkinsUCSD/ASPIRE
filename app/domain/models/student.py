from typing import Optional, List, Annotated, Literal
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, ARRAY, Integer

class StudentBase(SQLModel):
    student_id: int = Field(sa_column=Column("student_id", Integer, unique=True, primary_key=True))

class Student(StudentBase, table=True):
    pass

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    pass


class StudentToCourseBase(SQLModel):
    student_id: int = Field(foreign_key="student.student_id", primary_key=True)
    course_id: int = Field(foreign_key="course.course_id", primary_key=True)

class StudentToCourse(StudentToCourseBase, table=True):
    pass

class StudentToCourseRead(StudentToCourseBase):
    pass

class StudentToCourseCreate(StudentToCourseBase):
    pass


class StudentKnowledgeBase(SQLModel):
    student_id: int = Field(foreign_key="student.student_id", primary_key=True)
    concept_name: str = Field(foreign_key="concept.name", primary_key=True)

class StudentKnowledge(StudentKnowledgeBase, table=True):
    score: float = Field(default=0.0)

class StudentKnowledgeRead(StudentKnowledgeBase):
    score: Optional[float]

class StudentKnowledgeCreate(StudentKnowledgeBase):
    score: Optional[float]