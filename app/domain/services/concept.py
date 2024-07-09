from typing import List, Union, Literal
from fastapi import Depends

from app.domain.models.concept import (
    ConceptCreate, 
    ConceptRead, 
    ConceptToDomainCreate, 
    ConceptToDomainRead, 
    ConceptCreateBulkRead,
    ConceptToModuleRead,
    ConceptToModuleCreate,
    ConceptToConceptCreate,
    ConceptToConceptRead,
    ConceptBulkRead,
    ConceptFilter,
    ConceptReadVerbose,
    ConceptToModuleDelete,
    ConceptToConceptDelete
    )
from app.domain.protocols.repositories.concept import (
    ConceptRepository as ConceptRepoProtocol,
    ConceptToConceptRepository as CToCRepoProtocol, 
    ConceptToDomainRepository as CToDRepoProtocol,
    ConceptToModuleRepository as CToMRepoProtocol
    )
from app.domain.protocols.services.concept import (
    ConceptService as ConceptServiceProtocol, 
    ConceptToDomainService as CToDServiceProtocol,
    ConceptToModuleService as CToMServiceProtocol,
    ConceptToConceptService as CToCServiceProtocol
    )
from app.infrastructure.database.repositories.concept import (
    ConceptRepository, 
    ConceptToDomainRepository, 
    ConceptToModuleRepository,
    ConceptToConceptRepository
    )


class ConceptService(ConceptServiceProtocol, CToDServiceProtocol, CToMServiceProtocol, CToCServiceProtocol):
    def __init__(
        self, 
        concept_repo: ConceptRepoProtocol = Depends(ConceptRepository),
        c_to_d_repo: CToDRepoProtocol = Depends(ConceptToDomainRepository),
        c_to_m_repo: CToMRepoProtocol = Depends(ConceptToModuleRepository),
        c_to_c_repo: CToCRepoProtocol = Depends(ConceptToConceptRepository),
    ):
        
        self.concept_repo = concept_repo
        self.c_to_d_repo = c_to_d_repo
        self.c_to_m_repo = c_to_m_repo
        self.c_to_c_repo = c_to_c_repo
    

    async def create_concept(self, concept: ConceptCreate) -> ConceptRead:
        return await self.concept_repo.add(concept)
    

    async def bulk_create_concepts(self, concepts: List[ConceptCreate]) -> ConceptCreateBulkRead:
        concepts_result = await self.concept_repo.bulk_add(concepts=concepts)
        junctions_list = [ConceptToDomainCreate(concept_name=val.name, domain_id=val.domain_id) for val in concepts]

        await self.c_to_d_repo.bulk_add(junctions=junctions_list)

        return concepts_result


    async def get_concept(self, concept_name: str, read_mode: Literal["normal", "verbose"] = "normal") -> Union[ConceptRead, ConceptReadVerbose]:
        return await self.concept_repo.get_one(concept_name=concept_name, read_mode=read_mode)
        

    async def get_many_concepts(self, filters: ConceptFilter, read_mode: Literal["normal", "verbose"] = "normal") -> Union[ConceptBulkRead, List[ConceptReadVerbose]]:
        return await self.concept_repo.get_many(filters=filters, read_mode=read_mode)
    

    async def get_domain_init_concepts(self, course_id:int) -> ConceptBulkRead:
        return await self.concept_repo.get_many(filters=ConceptFilter(course_id=course_id), domain_init_mode=True)


    async def init_module_concepts(
            self, 
            module_id: int, 
            llm_concepts: List[ConceptCreate],
            llm_junctions: List[ConceptToConceptCreate],
            module_concepts: List[str]
    ) -> ConceptCreateBulkRead:
        
        concept_results = await self.bulk_create_concepts(concepts=llm_concepts)

        if concept_results.success and concept_results.failed:
            concept_results.success.extend([ConceptRead(name=val.object_id) for val in concept_results.failed if val.cause == "UniqueViolation"])
            all_concepts = concept_results.success
            
        elif concept_results.failed:
            all_concepts = [ConceptRead(name=val.object_id) for val in concept_results.failed if val.cause == "UniqueViolation"]

        else:
            all_concepts = concept_results.success

        module_junctions = [ConceptToModuleCreate(concept_name=val.name, module_id=module_id) for val in all_concepts if val.name in module_concepts]

        await self.bulk_create_module_junctions(junctions=module_junctions)

        await self.bulk_create_concept_junctions(junctions=llm_junctions)

        return concept_results

    # ConceptToDomain Service
    async def get_all_concepts_in_domain(self, domain_id: int) -> ConceptBulkRead:
        return await self.c_to_d_repo.get_all(domain_id=domain_id)
    
    
    async def create_domain_junction(self, junction: ConceptToDomainCreate) -> ConceptToDomainRead:
        return await self.c_to_d_repo.add(junction=junction)


    async def bulk_create_domain_junctions(self, junctions: List[ConceptToDomainCreate]) -> list[ConceptToDomainRead]:
        return await self.c_to_d_repo.bulk_add(junctions=junctions)


    # ConceptToModule Service
    async def bulk_create_module_junctions(self, junctions: List[ConceptToModuleCreate]) -> list[ConceptToModuleRead]:
        return await self.c_to_m_repo.bulk_add(junctions=junctions)
    

    async def get_all_concepts_in_module(self, module_id: int) -> ConceptBulkRead:
        return await self.c_to_m_repo.get_all(module_id=module_id)


    async def get_all_prereqs_of_module(self, module_id: int)-> ConceptBulkRead:
        module_concepts = await self.c_to_m_repo.get_all(module_id=module_id)
        module_concept_junctions = await self.c_to_c_repo.get_some(concepts=module_concepts)

        module_concept_list = [val.name for val in module_concepts.concepts]
        prereq_list = list(set([val.prereq_name for val in module_concept_junctions]))

        return ConceptBulkRead(concepts=[ConceptRead(name=val) for val in prereq_list if val not in module_concept_list])


    async def delete_module_junctions(self, junctions: List[ConceptToModuleDelete]):
        await self.c_to_m_repo.delete(junctions=junctions)


    # ConceptToConcept Service
    async def bulk_create_concept_junctions(self, junctions: List[ConceptToConceptCreate]) -> List[ConceptToConceptRead]:
        return await self.c_to_c_repo.bulk_add(junctions=junctions)
    
    async def get_concept_junctions(self, concepts: ConceptBulkRead, junction_direction: Literal["up", "down", "both"]="down") -> List[ConceptToConceptRead]:
        return await self.c_to_c_repo.get_some(concepts=concepts, junction_direction=junction_direction)

    async def delete_junctions(self, junctions: List[ConceptToConceptDelete]):
        await self.c_to_c_repo.delete(junctions=junctions)