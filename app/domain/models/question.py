from typing import Optional, List, Annotated, Literal
from datetime import date
from sqlmodel import Field, SQLModel, Column, ARRAY, Integer

class AnswerBase(SQLModel):
    # Not required from LLM
    answer_text: str
    # 100 if correct, 0 if incorrect
    answer_weight: int

class AnswerBaseExtended(AnswerBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: Optional[int] = Field(foreign_key="question.id")

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
    correct_comments: Optional[str]
    incorrect_comments: Optional[str]
    neutral_comments: Optional[str]

class Question(QuestionBase, table=True):
    pass

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
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