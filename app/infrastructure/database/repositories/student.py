from typing import List
import logging

from app.domain.models.concept import ConceptBulkRead

from app.domain.models.student import (
    StudentCreate, 
    StudentRead, 
    Student, 
    StudentKnowledgeCreate, 
    StudentKnowledgeRead, 
    StudentKnowledge, 
    StudentToCourseCreate, 
    StudentToCourseRead, 
    StudentToCourse
    )

from app.infrastructure.database.db import get_db
from sqlmodel import Session, select, col

from sqlalchemy.orm.attributes import flag_modified

from app.app.errors.db_error import DBError

logger = logging.getLogger(__name__)

class StudentRepository():
    db: Session
    
    def __init__(self):
        self.db = get_db()

    async def add(self, student: StudentCreate) -> StudentRead:
        try:
            student_obj = Student.from_orm(student)
            self.db.add(student_obj)
            self.db.commit()
            self.db.refresh(student_obj)

            return StudentRead.from_orm(student_obj)
        
        except Exception as e:
            logger.exception(msg="Failed to add Student.")
            raise DBError(
                origin="StudentRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add Student."
            ) from e

    async def get(self, canvas_id: str) -> StudentRead:
        return self.db.exec(
            select(Student).where(col(Student.canvas_id) == canvas_id)
        ).first()

class StudentToCourseRepository():
    db: Session
    
    def __init__(self):
        self.db = get_db()

    async def add(self, junction: StudentToCourseCreate) -> StudentToCourseRead:
        try:
            junction_obj = StudentToCourse.from_orm(junction)
            self.db.add(junction_obj)
            self.db.commit()
            self.db.refresh(junction_obj)

            return StudentToCourseRead.from_orm(junction_obj)
        
        except Exception as e:
            logger.exception(msg="Failed to add Student to course.")
            raise DBError(
                origin="StudentToCourseRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add Student to course."
            ) from e    


class StudentKnowledgeRepository():
    db: Session
    
    def __init__(self):
        self.db = get_db()

    async def get(self, student_id:int, concept_name:str) -> StudentKnowledgeRead:
        try:
            stmt = select(StudentKnowledge).where(StudentKnowledge.concept_name == concept_name).where(StudentKnowledge.student_id == student_id)
            return self.db.exec(stmt).one_or_none()
        
        except Exception as e:
            logger.exception(msg=f"Failed to retrieve student knowledge with student_id: {student_id} and concept_name: {concept_name}")
            raise DBError(
                origin="StudentKnowledgeRepository.get",
                type="QueryExecError",
                status_code=500,
                message=f"Failed to retrieve student knowledge with student_id: {student_id} and "
                        f"concept_name: {concept_name}, {e}"
            ) from e

    async def bulk_get(self, student_id: int, concept_list: List[str]) -> List[
        StudentKnowledgeRead]:
        try:
            stmt = select(StudentKnowledge).where(
                col(StudentKnowledge.concept_name).in_(concept_list)).where(
                col(StudentKnowledge.student_id) == student_id)
            result = self.db.exec(statement=stmt)
            result = StudentKnowledgeRead.from_orm(result.all())
            self.db.close()
            return result

        except Exception as e:
            logger.exception(
                msg=f"Failed to retrieve student knowledge with student_id: {student_id} and "
                    f"concepts: {concept_list}")
            raise DBError(
                origin="StudentKnowledgeRepository.get",
                type="QueryExecError",
                status_code=500,
                message=f"Failed to retrieve student knowledge with student_id: {student_id} and "
                        f"concepts: {concept_list}, {e}"
            ) from e

    async def add(self, score: StudentKnowledgeCreate) -> StudentKnowledgeRead:
        try:
            knowledge_obj = StudentKnowledge.from_orm(score)
            self.db.add(knowledge_obj)
            self.db.commit()
            self.db.refresh(knowledge_obj)
            result = StudentKnowledgeRead.from_orm(knowledge_obj)
            self.db.close()
            return result
        
        except Exception as e:
            logger.exception(msg="Failed add new student knowledge entry.")
            raise DBError(
                origin="StudentKnowledgeRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed add new student knowledge entry."
            ) from e
    
    async def update(self, score: StudentKnowledgeCreate) -> StudentKnowledgeRead:
        try:
            stmt = select(StudentKnowledge).where(StudentKnowledge.concept_name == score.concept_name).where(StudentKnowledge.student_id == score.student_id)
            result = self.db.exec(statement=stmt)

            knowledge = result.one_or_none()
            knowledge.score = score.score
            knowledge.no_of_inputs = score.no_of_inputs
            knowledge.numerator = score.numerator
            knowledge.denominator = score.denominator


            self.db.add(knowledge)

            # flag_modified(knowledge, 'change_history')
            self.db.commit()

            self.db.refresh(knowledge)
            result = StudentKnowledgeRead.from_orm(knowledge)

            self.db.close()
            return result
    
        except Exception as e:
            logger.exception(msg="Failed update student knowledge entry.")
            raise DBError(
                origin="StudentKnowledgeRepository.update",
                type="QueryExecError",
                status_code=500,
                message="Failed update student knowledge entry."
            ) from e

    async def get_many(self, concepts: ConceptBulkRead, student_id: int) -> List[StudentKnowledgeRead]:
        concept_list = [concept.name for concept in concepts.concepts]
        try:
            stmt = select(StudentKnowledge).where(StudentKnowledge.student_id == student_id).filter(StudentKnowledge.concept_name.in_(concept_list))
            result = self.db.exec(statement=stmt)
            result = result.all()

            return [StudentKnowledgeRead.from_orm(item) for item in result]
        
        except Exception as e:
            logger.exception(msg="Failed retrieve student knowledge entries.")
            raise DBError(
                origin="StudentKnowledgeRepository.get_many",
                type="QueryExecError",
                status_code=500,
                message="Failed retrieve student knowledge entries."
            ) from e