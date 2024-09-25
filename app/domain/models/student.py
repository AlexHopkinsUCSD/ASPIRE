from typing import Optional, List, Annotated, Literal, Dict
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, ARRAY, Integer, JSON, String

from sqlalchemy import event
from sqlalchemy.orm.attributes import flag_modified

import json

class StudentBase(SQLModel):
    id: Optional[int] = Field(sa_column=Column("student_id", Integer, unique=True, primary_key=True))
    # Anonymized Canvas ID
    # TODO: Create an Index on this.
    canvas_id: Optional[str] = Field(...)


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
    numerator: float
    denominator: float
    score: float = Field(default=0.5, le=1.0, ge=0.0)
    no_of_inputs: Optional[int] = Field(default=0)
    change_history: Optional[List[Dict[str, str]]] = Field(sa_column=Column("change_history", JSON(), nullable=True))


class StudentKnowledge(StudentKnowledgeBase, table=True):
    pass

class StudentKnowledgeRead(StudentKnowledgeBase):
    pass

class StudentKnowledgeCreate(StudentKnowledgeBase):
    pass


def update_change_history(mapper, connection, target):
    if target.change_history is None:
        target.change_history = []

    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "score": target.score,
        "no_of_inputs": target.no_of_inputs
        
    }
    flag_modified(target, 'change_history')
    target.change_history.append(new_entry)
    


event.listen(StudentKnowledge, 'before_insert', update_change_history)
event.listen(StudentKnowledge, 'before_update', update_change_history)