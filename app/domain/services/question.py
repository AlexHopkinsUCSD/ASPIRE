from typing import List, Union, Optional

from fastapi import Depends, UploadFile
from app.domain.models.question import QuestionAnswerInput, QuestionRead
from app.domain.protocols.repositories.question import QuestionRepository as QuestionRepoProtocol, AnswerRepository as AnswerRepoProtocol
from app.domain.protocols.services.question import QuestionService as QuestionServiceProtocol
from app.infrastructure.database.repositories.question import QuestionRepository, AnswerRepository
from app.domain.models.question import QuestionCreate, AnswerCreate

class QuestionService(QuestionServiceProtocol):
    def __init__(
            self, 
            question_repo: QuestionRepoProtocol = Depends(QuestionRepository), 
            answer_repo: AnswerRepoProtocol = Depends(AnswerRepository)
    ):
        self.question_repo = question_repo
        self.answer_repo = answer_repo

    async def create_question(self, question: QuestionAnswerInput) -> QuestionRead:
        ...

    async def create_questions(self, questions: List[QuestionAnswerInput]) -> List[QuestionRead]:
        
        result_list = []
        for entry in questions:
            result = await self.question_repo.add(entry.question)
            result_list.append(result)
            for answer in entry.answers:
                answer = AnswerCreate(**answer.dict(), question_id=result.id)
                await self.answer_repo.add(answer)  
            
        return result_list

    async def get_question(self, question_id: int) -> QuestionRead:
        ...

    async def get_all_questions(self) -> List[QuestionRead]:
        ...

    # async def update_question(self, question_id: int, question_update: QuestionUpdate) -> QuestionRead:
    #     ...

    async def delete_question(self, question_id: int) -> None:
        ...