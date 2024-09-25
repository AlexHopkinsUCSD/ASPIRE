from typing import  Protocol

from app.domain.models.student import StudentCreate, StudentRead, StudentKnowledgeRead, StudentToCourseCreate, StudentToCourseRead


class StudentService(Protocol):
    async def add_student(self, student: StudentCreate) -> StudentRead:
        """
        Adds a new student to the db
        """
        pass

    async def get_student(self, canvas_id: str) -> StudentRead:
        ...
    
    async def add_student_to_course(self, student_id: int, course_id: int) -> StudentToCourseRead:
        """
        Adds an existing student to a course
        """
        pass

    async def get_student_knowledge_score(self, student_id: int, concept_name: str) -> StudentKnowledgeRead:
        """
        Returns a single StudentKnowledge entry matching the student_id and concept_name
        """
        pass