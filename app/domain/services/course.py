from typing import  List, Union, Literal
from fastapi import Depends

from app.domain.protocols.services.course import CourseService as CourseServiceProtocol
from app.domain.protocols.services.concept import ConceptService as ConceptServiceProtocol

from app.domain.protocols.repositories.course import CourseRepository as CourseRepoProtocol

from app.infrastructure.database.repositories.course import CourseRepository

from app.domain.services.concept import ConceptService

from app.domain.models.course import CourseRead, CourseCreate, CourseCreateAPI, CourseUpdate, CourseFilter, CourseReadVerbose
from app.domain.models.llm_agent import Validator, ContingencyFunctions
from app.domain.models.forms import RegistrationForm

from app.infrastructure.LLM.llm_agent import LLMAgent
from app.infrastructure.LLM.contingencies.general import check_valid_json
from app.infrastructure.LLM.contingencies.summarize import format_as_string
from app.infrastructure.LLM.contingencies.domain_concepts import format_as_concept_create

class CourseService(CourseServiceProtocol):
    def __init__(
            self, 
            course_repo: CourseRepoProtocol = Depends(CourseRepository),
            concept_service: ConceptServiceProtocol = Depends(ConceptService),

    ):
        self.course_repo = course_repo
        self.concept_service = concept_service


    async def create_course(
            self,
            content_files, 
            model_name,
            form_data: RegistrationForm,
            domain_is_new: bool=False,
    ) -> CourseRead:
        
        llm_agent = LLMAgent(content_files=content_files)
        
        validators = [Validator(order=1, error_response="Invalid JSON", function=check_valid_json)]
        c_func = ContingencyFunctions(validators=validators, formatter=format_as_string)

        course_summary = await llm_agent.execute(action="summarize", contingency_functions=c_func, params= {"model_name": model_name})
        
        course_data = CourseCreate(**form_data.dict(), course_summary=course_summary)
        course = await self.course_repo.add(course=course_data)

        if domain_is_new:
            await llm_agent.add_param(course_id=course.course_id)
            validators[0].status = "FAIL"
            c_func = ContingencyFunctions(validators=validators, formatter=format_as_concept_create)

            concepts = await llm_agent.execute(
                action="domain-concepts", 
                contingency_functions=c_func, 
                params={"domain_id": form_data.domain_id, "subject": form_data.subject, "difficulty": form_data.difficulty, "model_name": model_name}
                )
            print(concepts)
            await self.concept_service.bulk_create_concepts(concepts=concepts)
            
        return course


    async def create_course_no_llm(self, course: CourseCreateAPI) -> CourseRead:
        course = CourseCreate(**course.dict())
        return await self.course_repo.add(course=course)


    async def get_one_course(self, course_id: int, read_mode: Literal["normal", "verbose"] = "normal") -> Union[CourseRead, CourseReadVerbose]:
        return await self.course_repo.get_one(course_id=course_id, read_mode=read_mode)


    async def get_matching_courses(self, filters: CourseFilter) -> List[CourseReadVerbose]:
        return await self.course_repo.get_many(filters=filters)


    async def update_course(self, course_id: int, course_update: CourseUpdate) -> CourseReadVerbose:
        return await self.course_repo.update(course_id=course_id, course_update=course_update)


    async def delete_course(self, course_id: int):
        return await self.course_repo.delete(course_id=course_id)