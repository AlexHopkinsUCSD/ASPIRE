from fastapi import Depends

from app.domain.models.student import StudentCreate, StudentRead, StudentKnowledgeRead, StudentToCourseCreate, StudentToCourseRead
from app.infrastructure.database.repositories.student import StudentRepository, StudentKnowledgeRepository, StudentToCourseRepository
from app.domain.protocols.repositories.student import (
    StudentKnowledgeRepository as StudentKnowledgeRepoProtocol,
    StudentRepository as StudentRepoProtocol,
    StudentToCourseRepository as SToCRepoProtocol
    )
from app.domain.protocols.services.student import StudentService as StudentServiceProtocol


class StudentService(StudentServiceProtocol):
    def __init__(
        self, 
        student_repo: StudentRepoProtocol = Depends(StudentRepository),
        s_k_repo: StudentKnowledgeRepoProtocol = Depends(StudentKnowledgeRepository),
        s_to_c_repo: SToCRepoProtocol = Depends(StudentToCourseRepository)

    ):
        self.student_repo = student_repo
        self.s_k_repo = s_k_repo
        self.s_to_c_repo = s_to_c_repo

    async def add_student(self, student: StudentCreate) -> StudentRead:
        return self.student_repo.add(student=student)
    
    async def add_student_to_course(self, student_id: int, course_id: int) -> StudentToCourseRead:
        return self.s_to_c_repo.add(junction=StudentToCourseCreate(student_id=student_id, course_id=course_id))

    async def get_student_knowledge_score(self, student_id: int, concept_name: str) -> StudentKnowledgeRead:
        return self.s_k_repo.get(student_id=student_id, concept_name=concept_name)