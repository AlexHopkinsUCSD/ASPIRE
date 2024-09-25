from typing import Optional, List, Annotated, Literal, Dict
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, ARRAY, Integer
from sqlalchemy.dialects.postgresql import JSON


class QuizBase(SQLModel):
    quiz_id: Optional[int] = Field(
        sa_column=Column("quiz_id", Integer, unique=True, primary_key=True
        )
    )
    module_id: int = Field(foreign_key="module.module_id")
    course_id: int = Field(foreign_key="course.course_id")
    sme_input: Dict = Field(default={}, sa_column=Column(JSON))
    sme_importance: float = Field(default=0.0, le=1.0, ge=0.0)
    n_questions: int = Field(default=5, ge=1)
    quiz_type: str = Field(...)
    due_date: datetime


class Quiz(QuizBase, table=True):
    pass


class QuizResultBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.quiz_id", primary_key=True)
    student_id: int = Field(foreign_key="student.student_id", primary_key=True)
    correct: Optional[int] = Field(...)
    total: Optional[int] = Field(...)
    total_time_taken_secs: Optional[int]

class QuizResult(QuizResultBase, table=True):
    pass
