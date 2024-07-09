from typing import List, Protocol, Literal, Union
from app.domain.models.question import QuestionCreate, QuestionRead, AnswerCreate, AnswerRead, Question, Answer
from app.domain.protocols.repositories.question import QuestionRepository as QuestionRepoProtocol, AnswerRepository as AnswerRepoProtocol
from app.infrastructure.database.db import get_db
from sqlmodel import Session
from fastapi import Depends


class QuestionRepository(QuestionRepoProtocol):
    db: Session
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def add(self, question: QuestionCreate) -> QuestionRead:
        question = Question.from_orm(question)
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return QuestionRead.from_orm(question)

class AnswerRepository(AnswerRepoProtocol):
    db: Session
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def add(self, answer: AnswerCreate) -> AnswerRead:
        answer = Answer.from_orm(answer)
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return AnswerRead.from_orm(answer)
    
