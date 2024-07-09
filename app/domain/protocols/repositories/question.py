from typing import List, Protocol, Literal, Union
from app.domain.models.question import QuestionCreate, QuestionRead, AnswerCreate, AnswerRead

class QuestionRepository(Protocol):
    async def add(self, question: QuestionCreate) -> QuestionRead:
        ...

class AnswerRepository(Protocol):
    async def add(self, answer: AnswerCreate) -> AnswerRead:
        ...
    
