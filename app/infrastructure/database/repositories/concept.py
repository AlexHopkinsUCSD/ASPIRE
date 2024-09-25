import logging

from typing import List, Union, Literal

from psycopg2.errors import  ForeignKeyViolation
from sqlalchemy.exc import IntegrityError, StatementError
from sqlmodel import Session, text, bindparam, select, join, alias 

from app.infrastructure.database.db import get_db

from app.app.errors.db_error import DBError
from app.domain.models.errors import DBError as DBErrorObj

from app.domain.models.domain import Domain
from app.domain.models.course import Course
from app.domain.models.module import ModuleToCourse

from app.domain.models.concept import (
    Concept,
    ConceptRead, 
    ConceptCreate, 
    ConceptToDomainCreate, 
    ConceptToDomainRead, 
    ConceptToDomain, 
    ConceptCreateBulkRead,
    ConceptToModule,
    ConceptToModuleRead,
    ConceptToModuleCreate,
    ConceptToConceptCreate,
    ConceptToConceptRead, 
    ConceptToConcept,
    ConceptFilter,
    ConceptBulkRead,
    ConceptReadVerbose,
    ConceptToModuleDelete,
    ConceptToConceptDelete,
    ConceptReadPreformatted
    )
from app.domain.protocols.repositories.concept import (
    ConceptRepository as ConceptRepositoryProtocol, 
    ConceptToDomainRepository as CToDRepoProtocol,
    ConceptToModuleRepository as CToMRepoProtocol,
    ConceptToConceptRepository as CToCRepoProtocol
    )

logger = logging.getLogger(__name__)

class ConceptRepository(ConceptRepositoryProtocol):
    db: Session

    def __init__(self):
        self.db = get_db()

    async def add(self, concept: ConceptCreate) -> ConceptRead:
        """
        Creates a new Concept and a ConceptToDomain entry in the DB
        """
        query_template = """
                WITH x AS (
                    INSERT INTO concept(name, subject, difficulty) 
                    VALUES(:name, :subject, :difficulty) 
                    RETURNING name
                )
                INSERT INTO concepttodomain(concept_name, domain_id)
                SELECT name, :domain_id FROM x
                RETURNING concept_name AS name
            """

        compiled_query = text(query_template)
        query_params = dict(concept)

        try:
            result = self.db.exec(statement=compiled_query, params=query_params)
            result = ConceptRead(**result.mappings().all()[0])
            self.db.commit()
            return result
        
        except IntegrityError as e:
            logger.exception(msg="Failed to add Concept object direct result")
            raise DBError(
                origin="ConceptRepository.add", 
                type="ForeignKeyViolation" if isinstance(e.orig, ForeignKeyViolation) else "UniqueViolation",
                status_code=400,
                message=str(e.orig)
                ) from e


    async def bulk_add(self, concepts: List[ConceptCreate]) -> ConceptCreateBulkRead:
        """
        Creates a new Concept entry in the DB for each item in the list of concepts.
        Ignores and logs any unique value violations.
        """
        with self.db.begin():
            query_template = """
                INSERT INTO concept(name, subject, difficulty) 
                VALUES(:name, :subject, :difficulty) 
                RETURNING name
                """

            compiled_query = text(query_template)

            failed_inserts = []
            successful_inserts = []

            for obj in concepts:
                query_params = dict(obj)
                nested = self.db.begin_nested()

                try:   
                    results = self.db.exec(statement=compiled_query, params=query_params)
                    successful_inserts.extend([ConceptRead(**val) for val in results.mappings().fetchall()])
                    nested.commit()

                except IntegrityError as e:
                    failed_inserts.append(
                        DBErrorObj(
                            cause="UniqueViolation", 
                            object_id=obj.name
                            )
                        )
                    nested.rollback()
                except StatementError as e:
                    logger.warn(msg=f"Concept Formatting Error, missing required value(s): {obj}")
                    failed_inserts.append(
                        DBErrorObj(
                            cause="StatementError", 
                            object_id=str(obj)
                            )
                        )
                    nested.rollback()

            if failed_inserts:
                logger.warn(msg=f"Failed to add the following Concept object(s):\n{failed_inserts}")
            return ConceptCreateBulkRead(success=successful_inserts, failed=failed_inserts)


    async def get_one(self, concept_name: str, read_mode: Literal["normal", "verbose"] = "normal") -> Union[ConceptRead, ConceptReadVerbose]:
        try:
            query_stmt = text("SELECT * FROM concept WHERE name = :name")
            results = self.db.exec(statement=query_stmt, params={"name": concept_name})

            if read_mode == "normal":
                return ConceptRead(**results.mappings().fetchone())
            
            else:
                return ConceptReadVerbose(**results.mappings().fetchone())
            
        except Exception as e:
            logger.exception(msg="Failed to return concept object.")
            raise DBError(
                origin="ConceptToConceptRepository.get_one",
                type="QueryExecError",
                status_code=500,
                message="Failed to return concept object."
            ) from e  


    async def get_many(self, filters: ConceptFilter, domain_init_mode: bool=False, read_mode: Literal["normal", "verbose"] = "normal") -> Union[List[ConceptRead], List[ConceptReadVerbose]]:
        if domain_init_mode: 
            #TODO: Test that the updated query works
            subquery = select(Concept).join(Course, Domain.domain_id == Course.domain_id).where(Course.course_id == filters.course_id).subquery()
            statement = select(Concept).where(Concept.subject == subquery.c.subject).where(Concept.difficulty == subquery.c.difficulty)

        else:
            statement = select(Concept).distinct()
            concept_to_module_alias_a = alias(ConceptToModule)
            concept_to_module_alias_b = alias(ConceptToModule)

            for key, filter_clause in filters.dict(exclude_none=True).items():

                if key == "module_id":

                    statement = statement.join(
                        concept_to_module_alias_a, 
                        (concept_to_module_alias_a.c.module_id == filter_clause) 
                        & 
                        (concept_to_module_alias_a.c.concept_name == Concept.name)
                        )

                elif key == "course_id":

                    statement = statement.join(
                        concept_to_module_alias_b, 
                        Concept.name == concept_to_module_alias_b.c.concept_name
                            ).join(
                                ModuleToCourse, 
                                (ModuleToCourse.module_id == concept_to_module_alias_b.c.module_id) 
                                & 
                                (ModuleToCourse.course_id == filter_clause)
                                )

                else:
                    column = getattr(Concept, key)
                    statement = statement.where(column==filter_clause)

        try:
            results = self.db.exec(statement=statement)
            if read_mode == "normal":
                return [ConceptRead.from_orm(v) for v in results.fetchall()]
            
            else:
                return [ConceptReadVerbose.from_orm(v) for v in results.fetchall()]
        
        except Exception as e:
            logger.exception(msg=f"Failed to retrieve concept(s) with filters: {filters.dict()}.")
            raise DBError(
                origin="ConceptRepository.get_many", 
                type="QueryExecError", 
                status_code=500, 
                message="Failed to select concepts"
                ) from e


class ConceptToDomainRepository(CToDRepoProtocol):
    db: Session

    def __init__(self):
        self.db = get_db()


    async def add(self, junction: ConceptToDomainCreate) -> ConceptToDomainRead:
        try:
            db_junction = ConceptToDomain.from_orm(junction)
            self.db.add(db_junction)
            self.db.commit()
            self.db.refresh(db_junction)
            return ConceptToDomainRead(**dict(db_junction))
        
        except Exception as e:
            logger.exception(msg="Failed to add ConceptToDomain object.")
            raise DBError(
                origin="ConceptToDomainRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add domain junction"
            ) from e


    async def bulk_add(self, junctions: List[ConceptToDomainCreate]) -> List[ConceptToDomainRead]:
        with self.db.begin():
            query_stmt = """
                INSERT INTO concepttodomain(concept_name, domain_id)
                SELECT name as concept_name, :domain_id FROM concept WHERE name = :concept_name
                RETURNING concept_name, domain_id 
                """
            compiled_query = text(query_stmt)

            failed_inserts = []
            successful_inserts = []

            for obj in junctions:
                query_params = dict(obj)
                nested = self.db.begin_nested()

                try:   
                    results = self.db.exec(statement=compiled_query, params=query_params)
                    successful_inserts.extend([ConceptToDomainRead(**val) for val in results.mappings().fetchall()])
                    nested.commit()

                except IntegrityError:
                    failed_inserts.append(
                        DBErrorObj(
                            cause="UniqueViolation", 
                            object_id=obj.concept_name
                            )
                        )
                    nested.rollback()

            if failed_inserts:
                logger.warn(msg=f"Failed to add the following ConceptToDomain object(s):\n{failed_inserts}")

            return successful_inserts
        


    async def get_all(self, domain_id: int) -> ConceptBulkRead:
        try:
            query_stmt = text("SELECT concept_name FROM concepttodomain WHERE domain_id = :domain_id")
            result = self.db.exec(statement=query_stmt, params={"domain_id": domain_id})
            result = ConceptBulkRead(concepts=[ConceptRead(name=val["concept_name"]) for val in result.mappings().fetchall()])

            if not result:
                raise DBError(
                    origin="ConceptToDomainRepository.get_all",
                    type="ValueError",
                    status_code=404,
                    message="Domain has no concept junctions"
                )
            
            return result
    
        except Exception as e:
            logger.exception(msg=f"Failed to get ConceptToDomain object(s) at domain_id: {domain_id}.")
            raise DBError(
                origin="ConceptToDomainRepository.get_all",
                type="QueryExecError",
                status_code=500,
                message="Failed to get domain junctions"
            ) from e

class ConceptToModuleRepository(CToMRepoProtocol):
    db: Session

    def __init__(self):
        self.db = get_db()


    async def add(self, junction: ConceptToModuleCreate) -> ConceptToModuleRead:
        try:
            db_junction = ConceptToModule.from_orm(junction)
            self.db.add(db_junction)
            self.db.commit()
            self.db.refresh(db_junction)

            return ConceptToDomainRead(**dict(db_junction))
        
        except Exception as e:
            logger.exception(msg=f"Failed to add ConceptToModule object.")
            raise DBError(
                origin="ConceptToModuleRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add module junction"
            ) from e

    async def bulk_add(self, junctions: List[ConceptToModuleCreate]) -> List[ConceptToModuleRead]:
        try:
            db_junctions = [ConceptToModule(**junction.dict()) for junction in junctions]
            
            self.db.add_all(db_junctions)
            self.db.commit()

        except Exception as e:
            logger.exception(msg=f"Failed to add ConceptToModule object(s).")
            raise DBError(
                origin="ConceptToModuleRepository.bulk_add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add module junctions"
            ) from e
        
        try:
            for object in db_junctions:
                self.db.refresh(object)

            return [ConceptToModuleRead(**dict(val)) for val in db_junctions]
        
        except Exception as e:
            logger.exception(msg=f"Failed to return ConceptToModule object.")
            raise DBError(
                origin="ConceptToModuleRepository.bulk_add",
                type="ReturnError",
                status_code=500,
                message="Failed to return module junction objects"
            ) from e
        

    async def get_all(self, module_id: int) -> ConceptBulkRead:
        try:
            query_stmt = text("SELECT concept_name FROM concepttomodule WHERE module_id = :module_id")
            result = self.db.exec(statement=query_stmt, params={"module_id": module_id})
            result = result.mappings().fetchall()
            if not result:
                raise DBError(
                    origin="ConceptToModuleRepository.get_all",
                    type="ReturnError",
                    status_code=404,
                    message=f"No concepts found at module_id: {module_id}"
                )
            
            return ConceptBulkRead(concepts=[ConceptRead(name=val["concept_name"]) for val in result])
        
        except Exception as e:
            logger.exception(msg=f"Failed to add ConceptToModule object(s) at module_id: {module_id}.")
            raise DBError(
                origin="ConceptToModuleRepository.get_all",
                type="QueryExecError",
                status_code=500,
                message="Failed to return module junction objects"
            ) from e  
        
    async def delete(self, junctions: List[ConceptToModuleDelete]):
        query_stmt = text("DELETE FROM concepttomodule WHERE module_id = :module_id AND concept_name = :concept_name")

        for item in junctions:
            try: 
                self.db.exec(statement=query_stmt, params=item.dict())
                self.db.commit()

            except Exception as e:
                logger.exception(msg=f"Failed to delete ConceptToModule object(s): {item}.")
                raise DBError(
                    origin="ConceptToModuleRepository.delete",
                    type="QueryExecError",
                    status_code=500,
                    message=f"Failed to delete ConceptToModule object(s): {item}"
                ) from e  


class ConceptToConceptRepository(CToCRepoProtocol):
    db: Session

    def __init__(self):
        self.db = get_db()


    async def add(self, junction: ConceptToConceptCreate) -> ConceptToConceptRead:
        try:
            db_junction = ConceptToConcept.from_orm(junction)

            self.db.add(db_junction)
            self.db.commit()
            self.db.refresh(db_junction)

            return ConceptToConceptRead(**dict(db_junction))
        
        except Exception as e:
            logger.exception(msg="Failed to add ConceptToConcept object.")
            raise DBError(
                origin="ConceptToConceptRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add concept junction"
            ) from e          


    async def bulk_add(self, junctions: List[ConceptToConceptCreate]) -> List[ConceptToConceptRead]:
        try:
            with self.db.no_autoflush as session:
                db_junctions = [ConceptToConcept.from_orm(junction) for junction in junctions]
                with session.begin(nested=True):
                    for obj in db_junctions:
                        nested = session.begin_nested()
                        try:
                            session.add(obj)
                            nested.commit()
                            session.refresh(obj)
                            
                        except IntegrityError as e:
                            nested.rollback()
                            
                result = [ConceptToConceptRead(**val.dict()) for val in db_junctions]
                session.commit()
                return result
        
        except Exception as e:
            logger.exception(msg="Failed to add ConceptToConcept object(s).")
            raise DBError(
                origin="ConceptToConceptRepository.bulk_add",
                type="QueryExecError",
                status_code=500,
                message="Failed to add concept junctions"
            ) from e  


    async def get_some(self, concepts: ConceptBulkRead, junction_direction: Literal["up", "down", "both"]="down") -> List[ConceptToConceptRead]:
        try:
            query_stmt_options = {
                "down": "SELECT * FROM concepttoconcept WHERE concept_name IN :concept_names;",
                "up": "SELECT * FROM concepttoconcept WHERE prereq_name IN :concept_names;",
                "both": "SELECT * FROM concepttoconcept WHERE concept_name IN :concept_names OR prereq_name IN :concept_names;"
            }
            query_params = {"concept_names": [val.name for val in concepts.concepts]}
            query_stmt = text(query_stmt_options[junction_direction]).bindparams(bindparam("concept_names", expanding=True))
            result = self.db.exec(statement=query_stmt, params=query_params)
            self.db.close()
            
            return [ConceptToConceptRead(**val) for val in result.mappings().fetchall()]
        
        except Exception as e:
            logger.exception(msg=f"Failed to get ConceptToConcept object(s) with direction: {junction_direction}.")
            raise DBError(
                origin="ConceptToConceptRepository.get_some",
                type="QueryExecError",
                status_code=500,
                message="Failed to retrieve concept junctions"
            ) from e    


    async def delete(self, junctions: List[ConceptToConceptDelete]):
        query_stmt = text("DELETE FROM concepttoconcept WHERE prereq_name = :prereq_name AND concept_name = :concept_name")

        for item in junctions:
            try: 
                self.db.exec(statement=query_stmt, params=item.dict())
                self.db.commit()

            except Exception as e:
                logger.exception(msg=f"Failed to delete ConceptToConcept object(s): {item}.")
                raise DBError(
                    origin="ConceptToConceptRepository.delete",
                    type="QueryExecError",
                    status_code=500,
                    message=f"Failed to delete ConceptToConcept object(s): {item}."
                ) from e  