import logging

from typing import List, Literal, Union

from sqlmodel import Session, text
from app.infrastructure.database.db import get_db

from app.app.errors.db_error import DBError
from app.domain.models.course import Course, CourseRead, CourseCreate, CourseFilter, CourseUpdate, CourseReadVerbose
from app.domain.protocols.repositories.course import CourseRepository as CourseRepositoryProtocol

logger = logging.getLogger(__name__)

class CourseRepository(CourseRepositoryProtocol):
    ''' 
    Provides data access to Course models.
    
    '''
    
    db: Session
    
    def __init__(self):
        self.db = get_db()


    async def add(self, course: CourseCreate) -> CourseRead:
        try:
            db_course = Course.from_orm(course)
            self.db.add(db_course)
            self.db.commit()
            self.db.refresh(db_course)
            return CourseRead.from_orm(db_course)
        
        except Exception as e:
            logger.exception(msg="Failed to add Course")
            raise DBError(
                origin="CourseRepository.add", 
                type=e.__class__.__name__, 
                status_code=400, 
                message=str(e.orig)
                ) from e
        

    async def get_one(self, course_id: int, read_mode: Literal["normal", "verbose"] = "normal") -> Union[CourseRead, CourseReadVerbose]:
        query_stmt = text("SELECT * FROM course WHERE course_id = :course_id")
        result = self.db.exec(statement=query_stmt, params={"course_id": course_id})
        result = result.mappings().fetchone()
        if not result:
            raise DBError(origin="CourseRepository.get_one", type="ValueError", status_code=404, message=f"Course with ID: {course_id} not found.")
        else:
            if read_mode == "verbose":
                return CourseReadVerbose(**result)
            else:
                return CourseRead(**result)
    

    async def get_many(self, filters: CourseFilter) -> List[CourseRead]:
        #TODO: Add more precise error handling
        try:
            if not filters.quarter and filters.quarter_filter:
                filters.quarter_filter = "equal"

            filters = filters.dict(exclude_none=True)

            query_stmt = "SELECT c.course_id, c.domain_id, c.name, c.quarter, c.instructor, c.course_summary FROM course AS c"
            course_where = []
            join_stmt = ["INNER JOIN domain ON domain.domain_id = c.domain_id"]
            params = {}

            for key, value in filters.items():
                if key == "quarter_filter":
                    continue

                if key in ["name", "instructor"]:
                    course_where.append(f"c.{key} = :{key}")
                    params[key] = value

                if key in ["subject", "difficulty"]:
                    join_stmt.append(f"domain.{key} = :{key}")
                    params[key] = value

                if key == "quarter":
                    date_options = {"equal": "=", "newer": ">", "older": "<", "newer-inclusive": ">=", "older-inclusive": "<="}
                    course_where.append(f"c.{key} {date_options[filters['quarter_filter']]} :{key}")
                    params[key] = value

            compiled_stmt = " ".join([query_stmt, " AND ".join(join_stmt), "WHERE" if course_where else "", " AND ".join(course_where)])
            result = self.db.exec(statement=text(compiled_stmt), params=params)

            return [CourseReadVerbose(**course) for course in result.mappings().all()]
        
        except Exception as e:
            logger.exception(msg="Failed to return Course(s)")
            raise DBError(
                origin="CourseRepository.get_many", 
                type=e.__class__.__name__, 
                status_code=400, 
                message=str(e.orig)
                ) from e
        

    async def update(self, course_id: int, course_update: CourseUpdate) -> CourseReadVerbose:
        try:
            set_stmt = []

            params = course_update.dict(exclude_none=True)
            for param in params.keys():
                set_stmt.append(f"{param} = :{param}")

            query_stmt = text(" ".join(["UPDATE course SET", " ,".join(set_stmt), "WHERE course_id = :course_id RETURNING *"]))
            params["course_id"] = course_id

            results = self.db.exec(statement=query_stmt, params=params)
            self.db.commit()

            return CourseReadVerbose(**results.mappings().fetchone())
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e
    

    async def delete(self, course_id: int):
        try:
            query_stmt = text("DELETE FROM course WHERE course_id = :course_id")

            results = self.db.exec(statement=query_stmt, params={"course_id": course_id})
            self.db.commit()

            # return CourseReadVerbose(**results.mappings().fetchone())
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e