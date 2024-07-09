from typing import List, Optional, Protocol
from app.domain.models.question import QuestionCreate, QuestionRead, AnswerPreCreate, QuestionAnswerInput

class QuestionService(Protocol):
    async def create_question(self, question: QuestionAnswerInput) -> QuestionRead:
        ...

    async def create_questions(self, questions: List[QuestionAnswerInput]) -> List[QuestionRead]:
        ...

    async def get_question(self, question_id: int) -> QuestionRead:
        ...

    async def get_all_questions(self) -> List[QuestionRead]:
        ...

    # async def update_question(self, question_id: int, question_update: QuestionUpdate) -> QuestionRead:
    #     ...

    async def delete_question(self, question_id: int) -> None:
        ...