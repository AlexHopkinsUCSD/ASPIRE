from typing import Protocol
from app.domain.models.student import (
    StudentCreate, 
    StudentRead, 
    StudentKnowledgeCreate, 
    StudentKnowledgeRead, 
    StudentToCourseCreate, 
    StudentToCourseRead, 
    )


class StudentRepository(Protocol):
    async def add(self, student: StudentCreate) -> StudentRead:
        """
        Adds a new student to the student table
        """
        pass


class StudentToCourseRepository(Protocol):
    async def add(self, junction: StudentToCourseCreate) -> StudentToCourseRead:
        """
        Adds a new junction between a student and a course
        """
        pass


class StudentKnowledgeRepository(Protocol):
    async def get(self, student_id:int, concept_name:str) -> StudentKnowledgeRead:
        """
        Returns a single StudentKnowledge entry matching the student_id and concept_name
        """
        pass
    
    async def add(self, score: StudentKnowledgeCreate) -> StudentKnowledgeRead:
        """
        Adds a new entry to the StudentKnowledge table
        """
        pass
    
    async def update(self, score: StudentKnowledgeCreate) -> StudentKnowledgeRead:
        """
        Updates the concept_score of an existing StudentKnowledge entry matching the student_id and concept_name provided in the StudentKnowledgeCreate object
        """
        pass