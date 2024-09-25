from datetime import date
from typing import Annotated, List, Literal, Optional

from sqlmodel import ARRAY, Column, Field, Integer, SQLModel


class AnswerBase(SQLModel):
    # Not required from LLM
    answer_text: str
    # 100 if correct, 0 if incorrect
    answer_weight: int
    # answer_feedback: str

class AnswerBaseExtended(AnswerBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: Optional[int] = Field(default=None, foreign_key="question.id")

class Answer(AnswerBaseExtended, table=True):
    pass

class QuestionBase(SQLModel):
    # TODO: Add a foreign key relation from the concept name.
    # Not required from LLM
    id: Optional[int] = Field(default=None, primary_key=True)
    # Not required from LLM
    position: int
    question_name: str
    # Not required from LLM
    question_type: str
    question_text: str
    # Not required from LLM
    points_possible: int
    neutral_comments: str

class Question(QuestionBase, table=True):
    pass

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase, table=True):
    pass

class AnswerRead(AnswerBaseExtended):
    pass

class AnswerPreCreate(AnswerBase):
    pass

class AnswerCreate(AnswerBaseExtended):
    pass


class QuestionAnswerInput(SQLModel):
    question: QuestionCreate
    answers: List[AnswerPreCreate]


class QuestionAnswerSelection(SQLModel):
    question: Question
    answers: List[AnswerRead]
