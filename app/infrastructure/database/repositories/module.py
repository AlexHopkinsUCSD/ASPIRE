import logging

from typing import Optional, List, Literal

from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from sqlmodel import Session, text

from app.infrastructure.database.db import get_db

from app.app.errors.db_error import DBError

from app.domain.protocols.repositories.module import ModuleRepository as ModuleRepoProtocol
from app.domain.models.module import ModuleRead, ModuleCreate, ModuleUpdate

logger = logging.getLogger(__name__)

class ModuleRepository(ModuleRepoProtocol):
    ''' 
    Provides data access to module models.
    '''
    
    db: Session
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def add(self, module: ModuleCreate) -> ModuleRead:
        query_template = """
                WITH x AS (
                    INSERT INTO module(domain_id, title, content_summary) 
                    VALUES(:domain_id, :title, :content_summary) 
                    RETURNING domain_id, module_id, title, content_summary
                ), y AS (
                    INSERT INTO moduletocourse(module_id, course_id)
                    SELECT module_id, :course_id FROM x
                )
                SELECT * FROM x
            """

        compiled_query = text(query_template)
        query_params = dict(module)

        try:
            result = self.db.exec(statement=compiled_query, params=query_params)

        except IntegrityError as e:
            raise DBError(
                origin="ModuleRepository.add", 
                type=e.__class__.__name__,
                status_code=400,
                message=str(e.orig)
                )
        
        try:
            result = ModuleRead(**result.mappings().all()[0])
            self.db.commit()
            return result
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.add",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e
    
    async def get_one(self, module_id: int) -> ModuleRead:
        try:
            query_stmt = text("SELECT * FROM module WHERE module_id = :module_id")
            result = self.db.exec(statement=query_stmt, params={"module_id": module_id})
            return ModuleRead(**result.mappings().fetchone())
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e
        
    async def get_all(self, filter_name: Literal["course", "domain", "all"], filter_id: Optional[int]=None) -> List[ModuleRead]:
        try:
            query_stmt = "SELECT module.module_id, title, domain_id, content_summary FROM module"
            filter_clause = ""
            params = {}
            if filter_name == "course":
                filter_clause = "INNER JOIN moduletocourse ON moduletocourse.module_id = module.module_id and moduletocourse.course_id = :course_id"
                params = {"course_id": filter_id}
            
            if filter_name == "domain":
                filter_clause = "WHERE domain_id = :domain_id"
                params = {"domain_id": filter_id}

            query_stmt = text(" ".join([query_stmt, filter_clause]))
            print(query_stmt)

            result = self.db.exec(statement=query_stmt, params=params)
            return [ModuleRead(**module) for module in result.mappings().all()]
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e
        
    async def update(self, module_id: int, module_update: ModuleUpdate) -> ModuleRead:
        try:
            query_stmt = "UPDATE module SET"
            set_stmts = " ,".join([
                "title = :title" if module_update.title else "", 
                "content_summary = :content_summary" if module_update.content_summary else ""
                ])
            query_stmt = text(" ".join([query_stmt, set_stmts, "WHERE module_id = :module_id RETURNING *"]))

            result = self.db.exec(statement=query_stmt, params={"module_id": module_id, **module_update.dict(exclude_none=True)})
            self.db.commit()
            
            return ModuleRead(**result.mappings().fetchone())
        
        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e
    
    async def delete_from_course(self, module_id: int, course_id: int) -> None:
        try:
            query_stmt = text("DELETE FROM moduletocourse WHERE module_id = :module_id AND course_id = :course_id")
            self.db.exec(statement=query_stmt, params={"module_id": module_id, "course_id": course_id})
            self.db.commit()

        except Exception as e:
            logger.exception(msg=f"Failed to return Module object.")
            raise DBError(
                origin="ModuleRepository.get_one",
                type="ReturnError",
                status_code=500,
                message="Failed return module"
            ) from e