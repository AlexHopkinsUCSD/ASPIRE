from typing import List, Union, Optional

from fastapi import Depends, UploadFile

from app.domain.models.forms import ModuleForm

from app.domain.protocols.repositories.module import ModuleRepository as ModuleRepoProtocol
from app.domain.protocols.services.module import ModuleService as ModuleServiceProtocol
from app.infrastructure.database.repositories.module import ModuleRepository
from app.domain.models.module import ModuleCreate, ModuleRead, ModuleUpdate, ModuleCreateNoLLM

from app.domain.models.concept import ConceptRead, ConceptToModuleCreate
from app.domain.protocols.services.concept import ConceptService as ConceptServiceProtocol, ConceptToModuleService as CToMProtocol
from .concept import ConceptService

from app.domain.protocols.services.course import CourseService as CourseServiceProtocol
from app.domain.services.course import CourseService

from app.domain.models.llm_agent import Validator, ContingencyFunctions

from app.infrastructure.LLM.llm_agent import LLMAgent
from app.infrastructure.LLM.contingencies.general import check_is_not_json, check_dict_values_not_json
from app.infrastructure.LLM.contingencies.summarize import format_as_string
from app.infrastructure.LLM.contingencies.module_concepts import format_for_module_concepts



class ModuleService(ModuleServiceProtocol):
    def __init__(
            self, 
            module_repo: ModuleRepoProtocol = Depends(ModuleRepository), 
            concept_service: Union[ConceptServiceProtocol, CToMProtocol] = Depends(ConceptService),
            course_service: CourseServiceProtocol = Depends(CourseService)
    ):
        self.module_repo = module_repo
        self.concept_service = concept_service
        self.course_service = course_service

    async def create_module(
            self,
            model_name,
            form_data: ModuleForm, 
            files: List[UploadFile],
            
    ) -> ModuleRead:
        """
        Used to automatically create a module and initialize it with concepts and prerequisites.\n
        Adds a new module to the DB and joins it to the domain and course.\n
        Uses the module content files from the SME to generate a summary of the module 
        as well as to identify all the concepts taught in a module and the dependent prerequisite concepts of each concept.\n
        Inserts all new module concepts to the DB as well as adding each new relationship to the module and domain.\n
        Inserts all new prereq concepts to the DB as well as adding each new relationship to other concepts and the domain.
        """
        #TODO: Error Handling
        llm_agent = LLMAgent(content_files=files, course_id=form_data.course_id)
        
        validators = [Validator(order=1, function=check_is_not_json)]
        c_func = ContingencyFunctions(validators=validators, formatter=format_as_string)
        content_summary = await llm_agent.execute(action="summarize", contingency_functions=c_func, params = {"model_name": model_name})

        course = await self.course_service.get_one_course(course_id=form_data.course_id)
        print(form_data.dict(exclude_none=True), content_summary, course)
        # test = ModuleCreate(module_id=1, title="ste", domain_id=1, content_summary="test", course_id=1)
        # print(test)
        module = ModuleCreate(title=form_data.title, course_id=form_data.course_id, content_summary=content_summary, domain_id=course.domain_id)
        result = await self.module_repo.add(module=module)


        validators = [
            Validator(order=1, function=check_is_not_json),
            Validator(order=2, function=check_dict_values_not_json)
            ]
        c_func = ContingencyFunctions(validators=validators, formatter=format_for_module_concepts)
        #TODO: Get subject and difficulty from domain
        llm_result = await llm_agent.execute(
            action="module-concepts", 
            contingency_functions=c_func, 
            params={"domain_id": course.domain_id, "subject": "comp-sci", "difficulty": 1, "model_name": model_name}
            )
        
        llm_concepts = llm_result[0]
        llm_junctions = llm_result[1]
        module_concepts = llm_result[2]

        await self.concept_service.init_module_concepts(
            module_id=result.module_id, 
            llm_concepts=llm_concepts, 
            llm_junctions=llm_junctions, 
            module_concepts=module_concepts
            )

        return result
    

    async def create_module_no_llm(self, module: ModuleCreateNoLLM, concepts: Optional[List[ConceptRead]]) -> ModuleRead:
        course = await self.course_service.get_one_course(course_id=module.course_id)
        module = ModuleCreate(**module.dict(), domain_id=course.domain_id)
        result = await self.module_repo.add(module=module)

        if concepts:
            junctions = [ConceptToModuleCreate(concept_name=concept.name, module_id=result.module_id) for concept in concepts]
            await self.concept_service.bulk_create_module_junctions(junctions=junctions)

        return result
    

    async def get_module(self, module_id: int) -> ModuleRead:
        return await self.module_repo.get_one(module_id=module_id)
    

    async def get_course_modules(self, course_id: int) -> List[ModuleRead]:
        return await self.module_repo.get_all(filter_name="course", filter_id=course_id)


    async def get_domain_modules(self, domain_id: int) -> List[ModuleRead]:
        return await self.module_repo.get_all(filter_name="domain", filter_id=domain_id)


    async def get_all_modules(self) -> List[ModuleRead]:
        return await self.module_repo.get_all(filter_name="all")
    

    async def update_module(self, module_id: int, module_update: ModuleUpdate) -> ModuleRead:
        return await self.module_repo.update(module_id=module_id, module_update=module_update)

    async def delete_module_from_course(self, module_id: int, course_id: int) -> None:
        return await self.module_repo.delete_from_course(module_id=module_id, course_id=course_id)